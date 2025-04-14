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

let selectedProduct = null;
let cartItems = [];

function showProductModal(productId, productName, price, description) {
    selectedProduct = {
        id: productId,
        name: productName,
        price: parseFloat(price),
        description: description
    };
    
    document.getElementById('productName').textContent = productName;
    document.getElementById('selectedPrice').textContent = `$${price}`;
    document.getElementById('productQuantity').value = 1;
    
    const modal = new bootstrap.Modal(document.getElementById('productModal'));
    modal.show();
}

function incrementQuantity(type) {
    const input = document.getElementById('productQuantity');
    input.value = parseInt(input.value) + 1;
}

function decrementQuantity(type) {
    const input = document.getElementById('productQuantity');
    if (parseInt(input.value) > 1) {
        input.value = parseInt(input.value) - 1;
    }
}

function addProductToCart() {
    const quantity = parseInt(document.getElementById('productQuantity').value);
    
    // Check if product already exists in cart
    const existingItem = cartItems.find(item => item.product_id === selectedProduct.id);
    
    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        cartItems.push({
            product_id: selectedProduct.id,
            name: selectedProduct.name,
            price: selectedProduct.price,
            quantity: quantity,
            discount: 0
        });
    }
    
    updateCartDisplay();
    bootstrap.Modal.getInstance(document.getElementById('productModal')).hide();
}

function updateCartDisplay() {
    const cartContainer = document.getElementById('cartItems');
    cartContainer.innerHTML = '';
    
    let subtotal = 0;
    
    cartItems.forEach((item, index) => {
        const itemTotal = (item.price * item.quantity) - item.discount;
        subtotal += itemTotal;
        
        cartContainer.innerHTML += `
            <div class="pos-cart-item">
                <div class="pos-cart-item-info">
                    <div class="pos-cart-item-title">${item.name}</div>
                    <div class="pos-cart-item-price">$${item.price.toFixed(2)} x ${item.quantity}</div>
                    ${item.discount > 0 ? `<div class="pos-cart-item-discount">Discount: $${item.discount.toFixed(2)}</div>` : ''}
                    <div class="pos-cart-item-total">$${itemTotal.toFixed(2)}</div>
                </div>
                <div class="pos-cart-item-actions">
                    <button class="btn btn-sm btn-outline-danger" onclick="removeFromCart(${index})">
                        <i class="bi bi-trash"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-theme" onclick="editItemDiscount(${index})">
                        <i class="bi bi-pencil"></i>
                    </button>
                </div>
            </div>
        `;
    });
    
    document.getElementById('subtotal').textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById('total').textContent = `$${subtotal.toFixed(2)}`;
}

function removeFromCart(index) {
    cartItems.splice(index, 1);
    updateCartDisplay();
}

function editItemDiscount(index) {
    const item = cartItems[index];
    const discount = prompt('Enter discount amount:', item.discount);
    if (discount !== null) {
        item.discount = parseFloat(discount) || 0;
        updateCartDisplay();
    }
}

function clearCart() {
    cartItems = [];
    updateCartDisplay();
}

function submitSale() {
    const customerId = document.getElementById('customerSelect').value;
    const location = document.getElementById('location').value;
    const notes = document.getElementById('paymentRemarks').value;
    
    if (!customerId) {
        alert('Please select a customer');
        return;
    }
    
    if (cartItems.length === 0) {
        alert('Please add items to cart');
        return;
    }
    
    const saleData = {
        customer_id: customerId,
        location: location,
        items: cartItems,
        notes: notes,
        payment_status: 'paid'
    };
    
    fetch('/create-sale/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(saleData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Sale completed successfully!');
            clearCart();
            document.getElementById('location').value = '';
            document.getElementById('paymentRemarks').value = '';
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        alert('Error creating sale: ' + error);
    });
}
