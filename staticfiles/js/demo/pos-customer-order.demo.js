/*
Template Name: HUD DJANGO - Responsive Bootstrap 5 Admin Template
Version: 2.4.0
Author: Sean Ngu
Website: http://www.seantheme.com/hud-django/
*/
var handleFilter = function() {
	"use strict";
	
	$(document).on('click', '.pos-menu [data-filter]', function(e) {
		e.preventDefault();
		
		var targetType = $(this).attr('data-filter');
		
		$(this).addClass('active');
		$('.pos-menu [data-filter]').not(this).removeClass('active');
		if (targetType == 'all') {
			$('.pos-content [data-type]').removeClass('d-none');
		} else {
			$('.pos-content [data-type="'+ targetType +'"]').removeClass('d-none');
			$('.pos-content [data-type]').not('.pos-content [data-type="'+ targetType +'"]').addClass('d-none');
		}
	});
};

document.addEventListener('DOMContentLoaded', function() {
	handleFilter();
});

// Update the product modal display
function showProductModal(productId, productName, stock) {
    // Store product details
    selectedProduct = {
        id: productId,
        name: productName,
        stock: parseInt(stock) || 0
    };
    
    // Update modal title
    document.getElementById('productName').textContent = productName;
    document.getElementById('productQuantity').value = 1;
    document.getElementById('productQuantity').max = stock;


    // Fetch price
    

    // Show the modal
    const modal = new bootstrap.Modal(document.getElementById('productModal'));
    modal.show();
}
