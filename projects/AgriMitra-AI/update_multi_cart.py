import re

# 1. Update common.js to add the cart generator function
with open('static/js/common.js', 'r', encoding='utf-8') as f:
    common_js = f.read()

cart_generator_code = '''
/* --- E-CART GENERATOR --- */
function generateEcartHTML(itemName, itemType) {
    let img1, img2, img3;
    let desc;
    if (itemType === 'seed') {
        img1 = "https://images.unsplash.com/photo-1593369165383-7c152a55097b?w=150&h=150&fit=crop";
        img2 = "https://images.unsplash.com/photo-1601493700631-2b16ec4b4716?w=150&h=150&fit=crop";
        img3 = "https://images.unsplash.com/photo-1592978340176-580a5611cd0e?w=150&h=150&fit=crop";
        desc = "High-yield seeds";
    } else {
        img1 = "https://images.unsplash.com/photo-1627916962295-d227dbb34ba1?w=150&h=150&fit=crop";
        img2 = "https://images.unsplash.com/photo-1585675100414-22d71f11e9df?w=150&h=150&fit=crop";
        img3 = "https://images.unsplash.com/photo-1592849008985-1d01990c7da7?w=150&h=150&fit=crop";
        desc = "Organic nutrients";
    }

    let base1 = 200 + (itemName.length * 10) + Math.round(Math.random() * 20);
    let base2 = base1 - 15 + Math.round(Math.random() * 30);
    let base3 = base1 + 10 + Math.round(Math.random() * 40);

    // 15% discount for AgriMitra Official
    let dp1 = Math.round(base1 * 0.85);

    return `
    <div class="ecart-widget" style="margin-top: 15px; background: white; border: 2px solid #22c55e; border-radius: 8px; overflow: hidden; width: 100%;">
        <div onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'block' : 'none';" style="background: #dcfce7; padding: 12px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; font-weight: bold; color: #166534; transition: 0.2s;">
            <span><i class="fa-solid fa-store"></i> Buy ${itemName} ${itemType === 'seed' ? 'Seeds' : ''} - View Sellers</span>
            <i class="fa-solid fa-caret-down"></i>
        </div>
        <div class="ecart-content" style="display: none; padding: 12px;">
            
            <!-- Seller 1 -->
            <div style="display: flex; gap: 10px; margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid #e5e7eb; align-items: center;">
                <img src="${img1}" style="width: 55px; height: 55px; object-fit: cover; border-radius: 6px; border: 1px solid #ccc;">
                <div style="flex: 1; line-height: 1.2;">
                    <div style="font-weight: bold; font-size: 13px; color: #111;">AgriMitra Official</div>
                    <div style="font-size: 11px; color: #059669; font-weight: bold;">Exclusive 15% Off</div>
                    <div style="font-size: 13px; font-weight: bold; color: #15803d; margin-top: 4px;">
                        <span style="text-decoration: line-through; color: #ef4444; font-size: 11px; margin-right:4px;">₹${base1}</span>₹${dp1}
                    </div>
                </div>
                <button onclick="showToast('Added ${itemName} (AgriMitra) to cart!', 'success')" style="background: #166534; color: white; border: none; border-radius: 4px; padding: 6px 10px; font-size: 11px; font-weight: bold; cursor: pointer;"><i class="fa-solid fa-cart-plus"></i> Add</button>
            </div>

            <!-- Seller 2 -->
            <div style="display: flex; gap: 10px; margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid #e5e7eb; align-items: center;">
                <img src="${img2}" style="width: 55px; height: 55px; object-fit: cover; border-radius: 6px; border: 1px solid #ccc;">
                <div style="flex: 1; line-height: 1.2;">
                    <div style="font-weight: bold; font-size: 13px; color: #111;">Ramesh Agro Dealers</div>
                    <div style="font-size: 11px; color: #6b7280;">Standard delivery</div>
                    <div style="font-size: 13px; font-weight: bold; color: #15803d; margin-top: 4px;">₹${base2}</div>
                </div>
                <button onclick="showToast('Added ${itemName} (Ramesh Agro) to cart!', 'success')" style="background: #2563eb; color: white; border: none; border-radius: 4px; padding: 6px 10px; font-size: 11px; font-weight: bold; cursor: pointer;"><i class="fa-solid fa-cart-plus"></i> Add</button>
            </div>

            <!-- Seller 3 -->
            <div style="display: flex; gap: 10px; align-items: center;">
                <img src="${img3}" style="width: 55px; height: 55px; object-fit: cover; border-radius: 6px; border: 1px solid #ccc;">
                <div style="flex: 1; line-height: 1.2;">
                    <div style="font-weight: bold; font-size: 13px; color: #111;">GreenLife Naturals</div>
                    <div style="font-size: 11px; color: #6b7280;">Verified Seller</div>
                    <div style="font-size: 13px; font-weight: bold; color: #15803d; margin-top: 4px;">₹${base3}</div>
                </div>
                <button onclick="showToast('Added ${itemName} (GreenLife) to cart!', 'success')" style="background: #2563eb; color: white; border: none; border-radius: 4px; padding: 6px 10px; font-size: 11px; font-weight: bold; cursor: pointer;"><i class="fa-solid fa-cart-plus"></i> Add</button>
            </div>

        </div>
    </div>
    `;
}
'''
if 'function generateEcartHTML' not in common_js:
    with open('static/js/common.js', 'a', encoding='utf-8') as f:
        f.write('\n' + cart_generator_code)


# 2. Update crop.js
with open('static/js/crop.js', 'r', encoding='utf-8') as f:
    crop_js = f.read()

crop_target = '''// Update E-Cart Section
                document.getElementById("ecartTitle").textContent = "Premium " + cropName + " Seeds";
                document.getElementById("ecartImg").src = "https://images.unsplash.com/photo-1593369165383-7c152a55097b?w=200&h=200&fit=crop";
                
                // Generate a deterministic random price
                let basePrice = 200 + (cropName.length * 10) + (Math.random() * 50);
                basePrice = Math.round(basePrice);
                let discountPrice = Math.round(basePrice * 0.85); // 15% off
                
                document.getElementById("ecartOldPrice").textContent = basePrice;
                document.getElementById("ecartNewPrice").textContent = discountPrice;'''

crop_replace = '''
                // Inject new dynamic multi-seller E-cart
                const ecartSection = document.getElementById("ecartSection");
                if (ecartSection) {
                    ecartSection.outerHTML = generateEcartHTML(cropName, 'seed');
                } else {
                    // In case it was already replaced, we can append it or find the new one.
                    // Actually, if it's replaced, its ID is gone. We need a stable container.
                    let container = document.getElementById("ecartContainer");
                    if (!container) {
                        container = document.createElement("div");
                        container.id = "ecartContainer";
                        document.querySelector(".result-card").appendChild(container);
                    }
                    container.innerHTML = generateEcartHTML(cropName, 'seed');
                }
'''
crop_js = crop_js.replace(crop_target, crop_replace)
with open('static/js/crop.js', 'w', encoding='utf-8') as f:
    f.write(crop_js)

# 3. Update fertilizer.js
with open('static/js/fertilizer.js', 'r', encoding='utf-8') as f:
    fert_js = f.read()

fert_target = '''// Update E-Cart Section
                document.getElementById("ecartTitle").textContent = fertName + " Organic Fertilizer";
                document.getElementById("ecartImg").src = "https://images.unsplash.com/photo-1627916962295-d227dbb34ba1?w=200&h=200&fit=crop";
                
                // Generate a deterministic random price
                let basePrice = 300 + (fertName.length * 15) + (Math.random() * 50);
                basePrice = Math.round(basePrice);
                let discountPrice = Math.round(basePrice * 0.85); // 15% off
                
                document.getElementById("ecartOldPrice").textContent = basePrice;
                document.getElementById("ecartNewPrice").textContent = discountPrice;'''

fert_replace = '''
                // Inject new dynamic multi-seller E-cart
                const ecartSection = document.getElementById("ecartSection");
                if (ecartSection) {
                    ecartSection.outerHTML = generateEcartHTML(fertName, 'fertilizer');
                } else {
                    let container = document.getElementById("ecartContainer");
                    if (!container) {
                        container = document.createElement("div");
                        container.id = "ecartContainer";
                        document.querySelector(".result-card").appendChild(container);
                    }
                    container.innerHTML = generateEcartHTML(fertName, 'fertilizer');
                }
'''
fert_js = fert_js.replace(fert_target, fert_replace)
with open('static/js/fertilizer.js', 'w', encoding='utf-8') as f:
    f.write(fert_js)


# 4. Update recommendation.html (Map Hub)
with open('templates/recommendation.html', 'r', encoding='utf-8') as f:
    rec_html = f.read()

# Replace the old static blocks in recommendation.html with the new dynamic function
# Using regex to replace the blocks we injected earlier

import re
rec_html = re.sub(
    r'let basePrice = 200.*?</button>.*?</div>.*?</div>.*?</div>`;', 
    'html += generateEcartHTML(d.crop, "seed");', 
    rec_html, 
    flags=re.DOTALL
)

rec_html = re.sub(
    r'let fertName = d\.fertilizer;.*?let basePrice = 300.*?</button>.*?</div>.*?</div>.*?</div>`;',
    'html += generateEcartHTML(d.fertilizer, "fertilizer");',
    rec_html,
    flags=re.DOTALL
)

with open('templates/recommendation.html', 'w', encoding='utf-8') as f:
    f.write(rec_html)

# Add cache busters
for filename in ['templates/crop.html', 'templates/fertilizer.html', 'templates/recommendation.html', 'templates/base.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    html = html.replace('js/crop.js\') }}?v=2', 'js/crop.js\') }}?v=3')
    html = html.replace('js/fertilizer.js\') }}?v=2', 'js/fertilizer.js\') }}?v=3')
    html = html.replace('js/common.js\') }}?v=2', 'js/common.js\') }}?v=3')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

print("Updated all files with dynamic multi-seller cart!")
