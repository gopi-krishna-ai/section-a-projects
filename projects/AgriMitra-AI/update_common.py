import re

with open('static/js/common.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Patch generateEcartHTML to pass product details
old_gen = """    } else {
        // Map DB fields to the format we need
        matches = matches.map(m => ({
            seller: m.seller,
            price: m.price,
            originalPrice: null,
            image_url: m.image_url,
            description: m.description
        }));
    }

    let itemsHTML = matches.map(m => {
        let origHTML = m.originalPrice ? `<span style="text-decoration: line-through; color: #ef4444; font-size: 11px; margin-right:4px;">₹${m.originalPrice}</span>` : "";
        return `
            <div style="display: flex; gap: 10px; margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid #e5e7eb; align-items: center;">
                <img src="${m.image_url}" style="width: 55px; height: 55px; object-fit: cover; border-radius: 6px; border: 1px solid #ccc;">
                <div style="flex: 1; line-height: 1.2;">
                    <div style="font-weight: bold; font-size: 13px; color: #111;">${m.seller}</div>
                    <div style="font-size: 11px; color: #6b7280;">${m.description}</div>
                    <div style="font-size: 13px; font-weight: bold; color: #15803d; margin-top: 4px;">
                        ${origHTML}₹${m.price}
                    </div>
                </div>
                <button onclick="addToCart('${itemName}', ${m.price}, '${m.image_url}', '${m.seller}')" style="background: #166534; color: white; border: none; border-radius: 4px; padding: 6px 10px; font-size: 11px; font-weight: bold; cursor: pointer;"><i class="fa-solid fa-cart-plus"></i> Add</button>
            </div>
        `;
    }).join("");"""

new_gen = """    } else {
        // Map DB fields to the format we need
        matches = matches.map(m => {
            let actualPrice = m.price;
            let orig = null;
            if (m.discount > 0) {
                orig = m.price;
                actualPrice = m.price - (m.price * m.discount / 100);
            }
            return {
                id: m.id,
                seller: m.seller,
                price: actualPrice,
                originalPrice: orig,
                image_url: m.image_url,
                description: m.description,
                stock: m.stock,
                discount: m.discount
            };
        });
    }

    let itemsHTML = matches.map(m => {
        let origHTML = m.originalPrice ? `<span style="text-decoration: line-through; color: #ef4444; font-size: 11px; margin-right:4px;">₹${m.originalPrice}</span>` : "";
        let discountTag = m.discount ? `<span style="background: #ef4444; color: white; padding: 2px 4px; border-radius: 3px; font-size: 9px; font-weight: bold; margin-left: 5px;">${m.discount}% OFF</span>` : "";
        let stockText = (m.stock !== undefined && m.stock <= 0) ? `<span style="color: #ef4444; font-size: 11px; font-weight:bold;">Out of Stock</span>` : `<span style="color: #6b7280; font-size: 10px;">Stock: ${m.stock !== undefined ? m.stock : '∞'}</span>`;
        
        let addBtn = (m.stock !== undefined && m.stock <= 0) 
            ? `<button disabled style="background: #9ca3af; color: white; border: none; border-radius: 4px; padding: 6px 10px; font-size: 11px; font-weight: bold; cursor: not-allowed;"><i class="fa-solid fa-ban"></i> Out</button>`
            : `<button onclick="addToCart('${itemName}', ${m.price}, '${m.image_url}', '${m.seller}', ${m.id || null})" style="background: #166534; color: white; border: none; border-radius: 4px; padding: 6px 10px; font-size: 11px; font-weight: bold; cursor: pointer;"><i class="fa-solid fa-cart-plus"></i> Add</button>`;

        return `
            <div style="display: flex; gap: 10px; margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid #e5e7eb; align-items: center;">
                <img src="${m.image_url}" style="width: 55px; height: 55px; object-fit: cover; border-radius: 6px; border: 1px solid #ccc;">
                <div style="flex: 1; line-height: 1.2;">
                    <div style="font-weight: bold; font-size: 13px; color: #111;">${m.seller} ${discountTag}</div>
                    <div style="font-size: 11px; color: #6b7280;">${m.description}</div>
                    <div style="font-size: 13px; font-weight: bold; color: #15803d; margin-top: 4px;">
                        ${origHTML}₹${m.price.toFixed(2)} <span style="margin-left: 5px;">${stockText}</span>
                    </div>
                </div>
                ${addBtn}
            </div>
        `;
    }).join("");"""

content = content.replace(old_gen, new_gen)

# Need to also patch addToCart signature and logic:
# `function addToCart(name, price, img, seller) {`
content = content.replace("function addToCart(name, price, img, seller) {", "function addToCart(name, price, img, seller, product_id) {")
content = content.replace("price: price,", "price: price,\n        product_id: product_id,")

# Now patch checkoutCart()
old_checkout = """        cart = [];
        saveCart();
        renderCartItems();
        updateCartBadge();
        
        alert("Order placed successfully! Check 'Track Orders' for details.");
        closeCart();"""

new_checkout = """
        let apiPayload = cart.map(item => ({
            product_id: item.product_id,
            quantity: item.unit === 'g' ? item.qty / 1000 : item.qty,
            price: calculateItemTotal(item.basePrice, item.qty, item.unit)
        }));

        fetch('/api/checkout', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({cart: apiPayload})
        }).then(r => r.json()).then(data => {
            if (data.success) {
                cart = [];
                saveCart();
                renderCartItems();
                updateCartBadge();
                alert("Order placed successfully!");
                closeCart();
            } else {
                alert("Failed: " + data.message);
            }
        }).catch(e => alert("Checkout error"));
"""
content = content.replace(old_checkout, new_checkout)

with open('static/js/common.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated common.js logic")
