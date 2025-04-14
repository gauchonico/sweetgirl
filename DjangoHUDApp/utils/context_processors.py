from django.urls import resolve

def mark_active_link(menu, current_path_name):
    for item in menu:
        item['is_active'] = item.get('name', '') == current_path_name

        if 'children' in item:
            item['children'] = mark_active_link(item['children'], current_path_name)

            if any(child.get('is_active', False) for child in item['children']):
                item['is_active'] = True

    return menu

def sidebar_menu(request):
	sidebar_menu = [{
		'text': 'Navigation',
		'is_header': 1
	},{
		'url': '/',
		'icon': 'bi bi-cpu',
		'text': 'Dashboard',
		'name': 'index'
	}, {
		'url': '/analytics',
		'icon': 'bi bi-bar-chart',
		'text': 'Analytics',
		'name': 'analytics'
	}, {
		'icon': 'bi bi-envelope',
		'text': 'Email',
		'children': [{
			'url': '/email/inbox',
			'action': 'Inbox',
			'text': 'Inbox',
			'name': 'emailInbox'
		}, {
			'url': '/email/compose',
			'action': 'Compose',
			'text': 'Compose',
			'name': 'emailCompose'
		}, {
			'url': '/email/detail',
			'action': 'Detail',
			'text': 'Detail',
			'name': 'emailDetail'
		}]
	}, {
		'is_divider': 1
	}, {
		'text': 'Components',
		'is_header': 1
	}, {
		'url': '/widgets',
		'icon': 'bi bi-columns-gap',
		'text': 'Widgets',
		'name': 'widgets'
	}, {
		'icon': 'bi bi-bag-check',
		'text': 'Products Management',
		'children': [{
			'url': '/products/',
			'text': 'Product Corner',
			'name': 'product_management'
		}, {
			'url': '/products/list/',
			'text': 'All Products',
			'name': 'product_list'
		}]
	}, {
		'is_divider': 1
	}]
	
	resolved_path = resolve(request.path_info)

	current_path_name = resolved_path.url_name
	
	sidebar_menu = mark_active_link(sidebar_menu, current_path_name)

	return {'sidebar_menu': sidebar_menu}