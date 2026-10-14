import re

with open('static/js/common.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Update checkoutCart function to prompt for address
old_checkout = """async function checkoutCart() {
    if (cart.length === 0) {
        alert("Your cart is empty!");
        return;
    }

    const apiPayload = cart.map(item => ({
        product_id: item.id,
        quantity: item.qty,
        price: item.price
    }));

    try {
        const res = await fetch('/api/checkout', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cart: apiPayload })
        });"""

new_checkout = """async function checkoutCart() {
    if (cart.length === 0) {
        alert("Your cart is empty!");
        return;
    }

    const address = prompt("Please enter your delivery location/address:");
    if (!address) {
        alert("Checkout cancelled: Delivery location is required.");
        return;
    }

    const apiPayload = cart.map(item => ({
        product_id: item.id,
        quantity: item.qty,
        price: item.price
    }));

    try {
        const res = await fetch('/api/checkout', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cart: apiPayload, address: address })
        });"""

js_content = js_content.replace(old_checkout, new_checkout)

with open('static/js/common.js', 'w', encoding='utf-8') as f:
    f.write(js_content)
print("Updated common.js with location prompt on checkout.")
