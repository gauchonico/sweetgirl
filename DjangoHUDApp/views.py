from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.db.models import Sum, F, Q
from django.views.decorators.http import require_POST
import json
from django.db import connection
from django.contrib.auth.decorators import login_required
import csv
from django.core.files.storage import default_storage
from .forms import ProductForm, BulkProductUploadForm, StockUpdateForm

from DjangoHUDApp.models import Customer, Product, Sale, SaleItem, Store, Category, ProductVariant

def index(request):
    context = {
    "appContentFullWidth": 1,
    
	}
    return render(request, "pages/index.html", context)

def analytics(request):
	return render(request, "pages/analytics.html")

def emailInbox(request):
	context = {
		"appContentFullHeight": 1,
		"appContentClass": "p-3"
	}
	return render(request, "pages/email-inbox.html", context)

def emailDetail(request):
	context = {
		"appContentFullHeight": 1,
		"appContentClass": "p-3"
	}
	return render(request, "pages/email-detail.html", context)

def emailCompose(request):
	context = {
		"appContentFullHeight": 1,
		"appContentClass": "p-3"
	}
	return render(request, "pages/email-compose.html", context)

def widgets(request):
	return render(request, "pages/widgets.html")

# create sale
def posCustomerOrder(request):
    search_query = request.GET.get('search', '')
    store_products = Product.objects.all()
    customers = Customer.objects.all()
    
    # search query
    if search_query:
        store_products = store_products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    context = {
        "store_products": store_products,
        "customers": customers,
        "search_query": search_query,
        'appSidebarHide': 1,
        'appHeaderHide': 1,
        'appContentFullHeight': 1,
        'appContentClass': "p-1 ps-xl-4 pe-xl-4 pt-xl-3 pb-xl-3",
    }
    return render(request, "pages/pos-customer-order.html", context)

@require_POST
def create_sale(request):
    try:
        data = json.loads(request.body)
        customer_id = data.get('customer_id')
        location = data.get('location')
        items = data.get('items', [])
        payment_status = data.get('payment_status', 'pending')
        notes = data.get('notes', '')

        # Create sale
        sale = Sale.objects.create(
            customer_id=customer_id,
            location=location,
            payment_status=payment_status,
            notes=notes
        )

        # Create sale items
        for item in items:
            product = Product.objects.get(id=item['product_id'])
            SaleItem.objects.create(
                sale=sale,
                product=product,
                quantity=item['quantity'],
                unit_price=product.price,
                discount=item.get('discount', 0)
            )

            # Update store quantity
            store, created = Store.objects.get_or_create(product=product)
            store.quantity -= item['quantity']
            store.save()

        return JsonResponse({
            'status': 'success',
            'sale_id': sale.id,
            'message': 'Sale created successfully'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def posKitchenOrder(request):
	context = {
		"appSidebarHide": 1, 
		"appHeaderHide": 1,  
		"appContentFullHeight": 1,
		"appContentClass": "p-1 ps-xl-4 pe-xl-4 pt-xl-3 pb-xl-3"
	}
	return render(request, "pages/pos-kitchen-order.html", context)

def posCounterCheckout(request):
	context = {
		"appSidebarHide": 1, 
		"appHeaderHide": 1,  
		"appContentFullHeight": 1,
		"appContentClass": "p-1 ps-xl-4 pe-xl-4 pt-xl-3 pb-xl-3"
	}
	return render(request, "pages/pos-counter-checkout.html", context)

def posTableBooking(request):
	context = {
		"appSidebarHide": 1, 
		"appHeaderHide": 1,  
		"appContentFullHeight": 1,
		"appContentClass": "p-1 ps-xl-4 pe-xl-4 pt-xl-3 pb-xl-3"
	}
	return render(request, "pages/pos-table-booking.html", context)

def posMenuStock(request):
	context = {
		"appSidebarHide": 1, 
		"appHeaderHide": 1,  
		"appContentFullHeight": 1,
		"appContentClass": "p-1 ps-xl-4 pe-xl-4 pt-xl-3 pb-xl-3"
	}
	return render(request, "pages/pos-menu-stock.html", context)

def uiBootstrap(request):
	return render(request, "pages/ui-bootstrap.html")

def uiButtons(request):
	return render(request, "pages/ui-buttons.html")

def uiCard(request):
	return render(request, "pages/ui-card.html")

def uiIcons(request):
	return render(request, "pages/ui-icons.html")

def uiModalNotifications(request):
	return render(request, "pages/ui-modal-notifications.html")

def uiTypography(request):
	return render(request, "pages/ui-typography.html")

def uiTabsAccordions(request):
	return render(request, "pages/ui-tabs-accordions.html")

def formElements(request):
	return render(request, "pages/form-elements.html")

def formPlugins(request):
	return render(request, "pages/form-plugins.html")

def formWizards(request):
	return render(request, "pages/form-wizards.html")

def tableElements(request):
	return render(request, "pages/table-elements.html")

def tablePlugins(request):
	return render(request, "pages/table-plugins.html")

def chartJs(request):
	return render(request, "pages/chart-js.html")

def chartApex(request):
	return render(request, "pages/chart-apex.html")

def map(request):
	return render(request, "pages/map.html")

def layoutStarter(request):
	return render(request, "pages/layout-starter.html")

def layoutFixedFooter(request):
	context = {
		"appFooter": 1
	}
	return render(request, "pages/layout-fixed-footer.html", context)

def layoutFullHeight(request):
	context = {
		"appContentFullHeight": 1,
		"appContentClass": "p-0"
	}
	return render(request, "pages/layout-full-height.html", context)

def layoutFullWidth(request):
	context = {
		"appContentFullWidth": 1,
		"appSidebarHide": 1
	}
	return render(request, "pages/layout-full-width.html", context)

def layoutBoxedLayout(request):
	context = {
		"appBoxedLayout": 1,
		"bodyClass": "pace-top"
	}
	return render(request, "pages/layout-boxed-layout.html", context)

def layoutCollapsedSidebar(request):
	context = {
		"appSidebarCollapsed": 1
	}
	return render(request, "pages/layout-collapsed-sidebar.html", context)

def layoutTopNav(request):
	context = {
		"appTopNav": 1,
		"appSidebarHide": 1
	}
	return render(request, "pages/layout-top-nav.html", context)

def layoutMixedNav(request):
	context = {
		"appTopNav": 1,
	}
	return render(request, "pages/layout-mixed-nav.html", context)

def layoutMixedNavBoxedLayout(request):
	context = {
		"appTopNav": 1,
		"appBoxedLayout": 1
	}
	return render(request, "pages/layout-mixed-nav-boxed-layout.html", context)

def pageScrumBoard(request):
	return render(request, "pages/page-scrum-board.html")

def pageProduct(request):
	return render(request, "pages/page-product.html")

def pageProductDetails(request):
	return render(request, "pages/page-product-details.html")

def pageOrder(request):
	return render(request, "pages/page-order.html")

def pageOrderDetails(request):
	return render(request, "pages/page-order-details.html")

def pageGallery(request):
	context = {
		"appContentFullHeight": 1,
		"appContentClass": 'p-0',
		"appSidebarCollapsed": 1
	}
	return render(request, "pages/page-gallery.html", context)

def pageSearchResults(request):
	return render(request, "pages/page-search-results.html")

def pageComingSoon(request):
	context = {
		"appSidebarHide": 1,
		"appHeaderHide": 1,
		"appContentClass": 'p-0'
	}
	return render(request, "pages/page-coming-soon.html", context)

def pageError(request):
	context = {
		"appSidebarHide": 1,
		"appHeaderHide": 1,
		"appContentClass": 'p-0'
	}
	return render(request, "pages/page-error.html", context)

def pageLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('DjangoHUDApp:analytics')
        else:
            messages.error(request, 'Invalid username or password.')
    
    context = {
        "appSidebarHide": 1,
        "appHeaderHide": 1,
        "appContentClass": 'p-0',
        "appContentFullWidth": 1,
        "appSidebarHide": 1,
        "appContentFullHeight": 1,
    }
    return render(request, "pages/page-login.html", context)

def pageRegister(request):
	context = {
		"appSidebarHide": 1,
		"appHeaderHide": 1,
		"appContentClass": 'p-0'
	}
	return render(request, "pages/page-register.html", context)

def pageMessenger(request):
	context = {
		"appContentFullHeight": 1,
		"appContentClass": 'p-3'
	}
	return render(request, "pages/page-messenger.html", context)

def pageDataManagement(request):
	context = {
		"appContentFullHeight": 1,
		"appContentClass": 'py-3'
	}
	return render(request, "pages/page-data-management.html", context)

def pageFileManager(request):
	context = {
		"appContentFullHeight": 1,
		"appContentClass": 'd-flex flex-column'
	}
	return render(request, "pages/page-file-manager.html", context)

def pagePricing(request):
	return render(request, "pages/page-pricing.html")

def profile(request):
	return render(request, "pages/profile.html")

def calendar(request):
	context = {
		"appContentFullHeight": 1,
		"appContentClass": "p-0"
	}
	return render(request, "pages/calendar.html", context)

def settings(request):
	return render(request, "pages/settings.html")

def helper(request):
	return render(request, "pages/helper.html")
	
def error404(request):
	context = {
		"appSidebarHide": 1,
		"appHeaderHide": 1,
		"appContentClass": 'p-0'
	}
	return render(request, "pages/page-error.html", context)

def handler404(request, exception = None):
	return redirect('/404/')

def logout_view(request):
    logout(request)
    return redirect('DjangoHUDApp:pageLogin')

def test_static(request):
    from django.conf import settings
    from django.contrib.staticfiles.finders import find
    import os
    
    context = {
        'static_root': settings.STATIC_ROOT,
        'static_url': settings.STATIC_URL,
        'static_dirs': settings.STATICFILES_DIRS,
        'vendor_css_exists': os.path.exists(os.path.join(settings.STATIC_ROOT, 'css', 'vendor.min.css')),
        'vendor_css_path': find('css/vendor.min.css'),
        'static_files': os.listdir(settings.STATIC_ROOT) if os.path.exists(settings.STATIC_ROOT) else [],
    }
    return render(request, 'test_static.html', context)

@login_required
def product_management(request, product_id=None):
    if product_id:
        product = get_object_or_404(Product, id=product_id)
    else:
        product = None

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.has_variants = request.POST.get('has_variants') == 'on'
            product.save()

            if product.has_variants:
                # Delete existing variants if any
                if product_id:
                    ProductVariant.objects.filter(product=product).delete()

                # Get variant data from form
                sizes = request.POST.getlist('variant_size[]')
                colors = request.POST.getlist('variant_color[]')
                stocks = request.POST.getlist('variant_stock[]')
                prices = request.POST.getlist('variant_price[]')

                # Create new variants
                for size, color, stock, price in zip(sizes, colors, stocks, prices):
                    if size and color:  # Only create if both size and color are provided
                        ProductVariant.objects.create(
                            product=product,
                            size=size,
                            color=color,
                            stock=int(stock),
                            price_adjustment=float(price)
                        )
            else:
                # If no variants, update the store quantity
                store, created = Store.objects.get_or_create(product=product)
                store.quantity = int(request.POST.get('stock', 0))
                store.save()

            messages.success(request, f'Product "{product.name}" saved successfully!')
            return redirect('DjangoHUDApp:product_list')
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
        'categories': Category.objects.all(),
    }
    return render(request, 'product_management.html', context)

@login_required
def download_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="product_template.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['name', 'price', 'stock', 'description', 'category'])
    writer.writerow(['Example Product', '99.99', '100', 'Product description', 'Category'])
    
    return response

@login_required
def product_list(request):
    products = Product.objects.all().order_by('name')
    context = {
        'products': products,
        'title': 'Product List'
    }
    return render(request, 'product_list.html', context)

@login_required
def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,
        'title': f'Product Details - {product.name}'
    }
    return render(request, 'product_details.html', context)

@login_required
def update_stock(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = StockUpdateForm()
    
    if request.method == 'POST':
        form = StockUpdateForm(request.POST)
        if form.is_valid():
            try:
                quantity = form.cleaned_data['quantity']
                operation = form.cleaned_data['operation']
                notes = form.cleaned_data['notes']
                
                if operation == 'add':
                    product.stock += quantity
                else:
                    product.stock = max(0, product.stock - quantity)
                
                product.save()
                messages.success(request, f'Stock updated successfully! New stock: {product.stock}')
                return redirect('DjangoHUDApp:product_details', product_id=product.id)
            except Exception as e:
                messages.error(request, f'Error updating stock: {str(e)}')
    
    context = {
        'product': product,
        'form': form,
        'title': f'Update Stock - {product.name}'
    }
    return render(request, 'update_stock.html', context)

@login_required
def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('DjangoHUDApp:product_list')
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'categories': categories,
    }
    return render(request, 'product_edit.html', context)

@login_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('DjangoHUDApp:product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})

@login_required
def store_view(request):
    # Get search query from request
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    # Start with all products
    products = Product.objects.all()
    
    # Apply search filter if exists
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Apply category filter if exists
    if category_filter:
        products = products.filter(category__id=category_filter)
    
    # Get all categories for the filter dropdown
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_filter,
        'appContentClass': 'p-3'
    }
    
    return render(request, 'pages/store.html', context)