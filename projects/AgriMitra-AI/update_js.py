import re

with open('static/js/common.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

# Add global product fetching at the top
fetch_code = """
let AGRI_PRODUCTS = [];
fetch('/api/products').then(res => res.json()).then(data => { AGRI_PRODUCTS = data; }).catch(e => console.error('Failed to load products', e));

/* --- E-CART GENERATOR --- */
"""
if 'let AGRI_PRODUCTS = [];' not in js_code:
    js_code = js_code.replace('/* --- E-CART GENERATOR --- */', fetch_code)

new_ecart = """function generateEcartHTML(itemName, itemType) {
    let matches = AGRI_PRODUCTS.filter(p => p.item_type === itemType && p.item_name.toLowerCase() === itemName.toLowerCase());
    
    // Fallback logic if admin didn't upload this product
    if (matches.length === 0) {
        let img1, img2, img3, desc;
        if (itemType === 'seed') {
            img1 = "https://placehold.co/200x200?text=Seeds+Premium";
            img2 = "https://placehold.co/200x200?text=Seeds+Pro";
            img3 = "https://placehold.co/200x200?text=Seeds+Standard";
            desc = "High-yield seeds";
        } else {
            img1 = "https://placehold.co/200x200?text=Organic+Fertilizer";
            img2 = "https://placehold.co/200x200?text=Mineral+Mix";
            img3 = "https://placehold.co/200x200?text=Compost";
            desc = "Organic nutrients";
        }

        let base1 = 200 + (itemName.length * 10) + Math.round(Math.random() * 20);
        let base2 = base1 - 15 + Math.round(Math.random() * 30);
        let base3 = base1 + 10 + Math.round(Math.random() * 40);
        let dp1 = Math.round(base1 * 0.85);
        
        matches = [
            { seller: "AgriMitra Official", price: dp1, originalPrice: base1, image_url: img1, description: desc + " - Exclusive 15% Off!" },
            { seller: "Ramesh Agro Dealers", price: base2, originalPrice: null, image_url: img2, description: "Standard delivery" },
            { seller: "GreenLife Naturals", price: base3, originalPrice: null, image_url: img3, description: "Verified Seller" }
        ];
    } else {
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
    }).join('');

    return `
    <div class="ecart-widget" style="margin-top: 15px; background: white; border: 2px solid #22c55e; border-radius: 8px; overflow: hidden; width: 100%;">
        <div onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'block' : 'none';" style="background: #dcfce7; padding: 12px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; font-weight: bold; color: #166534; transition: 0.2s;">
            <span><i class="fa-solid fa-store"></i> Buy ${itemName} ${itemType === 'seed' ? 'Seeds' : ''} - View Sellers</span>
            <i class="fa-solid fa-caret-down"></i>
        </div>
        <div class="ecart-content" style="display: none; padding: 12px;">
            ${itemsHTML}
        </div>
    </div>
    `;
}"""

# We need to replace the entire generateEcartHTML function
js_code = re.sub(r'function generateEcartHTML.*?return `.*?</div>\s+</div>\s+`;\s+}', new_ecart, js_code, flags=re.DOTALL)

with open('static/js/common.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("common.js updated with dynamic admin products support.")
