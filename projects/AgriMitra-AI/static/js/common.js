
function getCartKey() {
    return 'agriCart_' + (window.USER_ID || 'guest');
}

function saveCart() {
    localStorage.setItem(getCartKey(), JSON.stringify(cart));
    updateCartBadge();
}

function loadCart() {
    cart = JSON.parse(localStorage.getItem(getCartKey())) || [];
    updateCartBadge();
}

/* =============================================
   AGRIMITRA AI - COMMON UI LOGIC
   Sidebar/topbar translation + language events
   ============================================= */

const DEFAULT_LANG = "en";
const SUPPORTED = ["en", "kn", "hi", "te", "ta", "fr", "es"];

function getSavedLanguage() {
    const saved = localStorage.getItem("agri_language");
    if (SUPPORTED.includes(saved)) return saved;
    const serverLang = document.body.getAttribute("data-language");
    if (SUPPORTED.includes(serverLang)) return serverLang;
    return DEFAULT_LANG;
}

function saveLanguage(lang) {
    localStorage.setItem("agri_language", lang);
}

/* Persist the selected language to the Flask session so the choice survives
   navigation between pages (crop, fertilizer, soil, ...). */
function persistLanguage(lang) {
    try {
        fetch("/api/language", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ language: lang })
        }).catch(function () { /* offline is fine; localStorage still works */ });
    } catch (err) { /* ignore */ }
}

function applySidebarLanguage(lang) {
    return NLP.applyTo(lang, SIDEBAR_STRINGS).then(function () {
        document.dispatchEvent(new CustomEvent("agri:langchange", { detail: { lang: lang } }));
    });
}

const SIDEBAR_STRINGS = {
    appName: "AgriMitra AI",
    menuDashboard: "Dashboard",
    menuCrop: "Crop Recommendation",
    menuSoil: "Soil Analysis",
    menuFertilizer: "Fertilizer Recommendation",
    menuComplete: "Complete Recommendation",
    menuAI: "AI Assistant",
    menuHistory: "History",
    menuProfile: "Profile",
    menuSettings: "Settings",
    menuLogout: "Logout",
    menuLifecycle: "Crop Lifecycle",
    menuMarket: "Marketplace",
    subtitle: "Empowering Farmers with Artificial Intelligence",
    footer: "2026 AgriMitra AI | Made with Love for Farmers"
};

function setLanguageSelector(lang) {
    const sel = document.getElementById("language");
    if (sel && SUPPORTED.includes(lang)) sel.value = lang;
}

function initLanguage() {
    const sel = document.getElementById("language");
    if (!sel) return;

    // Prefer the language the user last chose (localStorage) so the choice
    // survives page navigation; fall back to the server-preferred language.
    let lang = getSavedLanguage();

    sel.value = lang;
    setTimeout(() => {
        const gtCombo = document.querySelector('.goog-te-combo');
        if (gtCombo) {
            gtCombo.value = lang;
            gtCombo.dispatchEvent(new Event('change'));
        }
    }, 1000); // wait for GT to load
    applySidebarLanguage(lang);

    sel.addEventListener("change", function () {
        const lang = this.value;
        saveLanguage(lang);
        persistLanguage(lang);
        
        // Trigger Google Translate widget for full page translation
        const gtCombo = document.querySelector('.goog-te-combo');
        if (gtCombo) {
            gtCombo.value = lang;
            gtCombo.dispatchEvent(new Event('change'));
        }
        
        // Let the existing NLP system do its sidebar/toast duties
        applySidebarLanguage(lang);
    });
}

document.addEventListener("DOMContentLoaded", initLanguage);

/* ---------- sidebar navigation ---------- */

document.addEventListener("DOMContentLoaded", function () {
    const PAGES = {
        dashboard: "/dashboard",
        crop: "/crop",
        soil: "/soil",
        fertilizer: "/fertilizer",
        recommendation: "/recommendation",
        lifecycle: "/lifecycle",
        market: "/market",
        assistant: "/assistant",
        history: "/history",
        profile: "/profile",
        admin: "/admin",
        settings: "/settings",
        logout: "/logout"
    };

    const current = document.body.getAttribute("data-page") || "";

    document.querySelectorAll(".sidebar li").forEach(function (li) {
        const page = li.getAttribute("data-page");
        if (page === current) {
            li.classList.add("active");
        } else {
            li.classList.remove("active");
        }
        li.addEventListener("click", function () {
            if (PAGES[page]) window.location.href = PAGES[page];
        });
        li.addEventListener("keydown", function (e) {
            if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                if (PAGES[page]) window.location.href = PAGES[page];
            }
        });
        li.style.cursor = "pointer";
    });
});

/* ---------- toast notifications ---------- */

function showToast(message, type) {
    type = type || "info";
    const stack = document.getElementById("toastStack");
    if (!stack) return;

    const icons = { success: "fa-circle-check", error: "fa-circle-exclamation", info: "fa-circle-info" };

    const toast = document.createElement("div");
    toast.className = "toast " + type;
    toast.setAttribute("role", "status");
    toast.innerHTML = '<i class="fa-solid ' + (icons[type] || icons.info) + '" aria-hidden="true"></i><span></span>';
    toast.querySelector("span").textContent = message;
    stack.appendChild(toast);

    setTimeout(function () {
        toast.classList.add("leaving");
        setTimeout(function () { toast.remove(); }, 200);
    }, 3500);
}



let AGRI_PRODUCTS = [];
fetch('/api/products').then(res => res.json()).then(data => { AGRI_PRODUCTS = data; }).catch(e => console.error('Failed to load products', e));

/* --- E-CART GENERATOR --- */

function generateEcartHTML(itemName, itemType) {
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
}



/* ===========================================
   CART SYSTEM LOGIC (PROFESSIONAL)
   =========================================== */

let cart = []; loadCart();

// Migrate old cart items
cart = cart.map(item => {
    if (item.price && !item.basePrice) item.basePrice = item.price;
    if (!item.qty) item.qty = 1;
    if (!item.unit) item.unit = 'kg';
    if (item.img && item.img.includes('wikimedia')) item.img = 'https://placehold.co/200x200?text=' + encodeURIComponent(item.title);
    return item;
});

localStorage.setItem(getCartKey(), JSON.stringify(cart));
let orders = JSON.parse(localStorage.getItem('agriOrders')) || [];

// Add overlay to body if not exists
document.addEventListener('DOMContentLoaded', () => {
    updateCartBadge();
    if (!document.getElementById('cartOverlay')) {
        const overlay = document.createElement('div');
        overlay.id = 'cartOverlay';
        overlay.className = 'cart-overlay';
        overlay.onclick = closeCart;
        document.body.appendChild(overlay);
    }
});

function toggleCart() {
    const sidebar = document.getElementById('cartSidebar');
    if (sidebar.classList.contains('open')) {
        closeCart();
    } else {
        openCart();
    }
}

function openCart() {
    const sidebar = document.getElementById('cartSidebar');
    const overlay = document.getElementById('cartOverlay');
    if (sidebar && overlay) {
        sidebar.classList.add('open');
        overlay.classList.add('open');
        renderCart();
        renderOrders();
    }
}

function closeCart() {
    const sidebar = document.getElementById('cartSidebar');
    const overlay = document.getElementById('cartOverlay');
    if (sidebar && overlay) {
        sidebar.classList.remove('open');
        overlay.classList.remove('open');
    }
}

function switchCartTab(tab) {
    document.querySelectorAll('.cart-tab').forEach(t => t.classList.remove('active'));
    if (tab === 'items') {
        document.getElementById('tabCartItems').classList.add('active');
        document.getElementById('cartItemsContainer').style.display = 'block';
        document.getElementById('cartOrdersContainer').style.display = 'none';
        document.getElementById('cartFooter').style.display = 'block';
    } else {
        document.getElementById('tabCartOrders').classList.add('active');
        document.getElementById('cartItemsContainer').style.display = 'none';
        document.getElementById('cartOrdersContainer').style.display = 'block';
        document.getElementById('cartFooter').style.display = 'none';
    }
}

function addToCart(title, basePrice, img, seller) {
    // Check if item already in cart
    const existing = cart.find(i => i.title === title && i.seller === seller);
    if (existing) {
        existing.qty += 1;
    } else {
        // basePrice is assumed to be per Kg
        cart.push({ id: Date.now(), title, basePrice, img, seller, qty: 1, unit: 'kg' });
    }
    
    localStorage.setItem(getCartKey(), JSON.stringify(cart));
    updateCartBadge();
    
    // Automatically open cart to show the added item
    switchCartTab('items');
    openCart();
}

function updateCartItem(id, field, value) {
    const item = cart.find(i => i.id === id);
    if (item) {
        if (field === 'qty') item.qty = parseFloat(value) || 1;
        if (field === 'unit') item.unit = value;
        localStorage.setItem(getCartKey(), JSON.stringify(cart));
        renderCart(); // Re-render to update subtotals
    }
}

function removeFromCart(id) {
    cart = cart.filter(item => item.id !== id);
    localStorage.setItem(getCartKey(), JSON.stringify(cart));
    updateCartBadge();
    renderCart();
}

function updateCartBadge() {
    const badge = document.getElementById('cartBadge');
    if (badge) {
        const totalItems = cart.reduce((acc, item) => acc + (item.unit === 'g' ? 1 : item.qty), 0);
        badge.innerText = cart.length; // Or totalItems if you want sum of qty
        badge.style.display = cart.length > 0 ? 'inline' : 'none';
    }
}

function calculateItemTotal(basePrice, qty, unit) {
    let price = parseFloat(basePrice);
    let q = parseFloat(qty);
    if (unit === 'g') {
        // If price is per Kg, 1 gram is price/1000
        return (price / 1000) * q;
    }
    return price * q;
}

function renderCart() {
    const container = document.getElementById('cartItemsContainer');
    if (!container) return;
    
    if (cart.length === 0) {
        container.innerHTML = `
            <div style="text-align:center; padding: 50px 20px;">
                <i class="fa-solid fa-cart-shopping" style="font-size: 4rem; color: #d1d5db; margin-bottom: 20px;"></i>
                <h3 style="color: #374151; margin-bottom: 10px;">Your cart is empty</h3>
                <p style="color: #6b7280; margin-bottom: 20px;">Looks like you haven't added any products to your cart yet.</p>
                <button onclick="closeCart()" style="padding: 10px 20px; background: var(--c-primary); color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold;">Continue Shopping</button>
            </div>
        `;
        document.getElementById('cartTotal').innerText = '₹0.00';
        return;
    }
    
    let html = '';
    let grandTotal = 0;
    
    cart.forEach(item => {
        let itemTotal = calculateItemTotal(item.basePrice, item.qty, item.unit);
        grandTotal += itemTotal;
        
        let qtyOptions = '';
        for(let i=1; i<=10; i++) {
            qtyOptions += `<option value="${i}" ${item.qty == i ? 'selected' : ''}>${i}</option>`;
        }
        // If qty is a custom number (e.g. they typed it), make sure it's selected
        if (item.qty > 10 || item.qty % 1 !== 0) {
            qtyOptions += `<option value="${item.qty}" selected>${item.qty}</option>`;
        }
        
        html += `
            <div class="cart-item">
                <img src="${item.img}" alt="${item.title}">
                <div class="cart-item-details">
                    <div class="cart-item-title">${item.title}</div>
                    <div class="cart-item-seller">Sold by: ${item.seller}</div>
                    <div class="cart-item-stock">In Stock</div>
                    <div class="cart-item-price">₹${item.basePrice} <span style="font-size:0.8rem; color:#6b7280; font-weight:normal;">/ kg</span></div>
                    
                    <div class="cart-controls">
                        <label style="font-size: 0.85rem; color: #374151; font-weight: 600;">Qty:</label>
                        <input type="number" min="0.1" step="0.1" style="width: 70px;" value="${item.qty}" onchange="updateCartItem(${item.id}, 'qty', this.value)">
                        
                        <select onchange="updateCartItem(${item.id}, 'unit', this.value)">
                            <option value="kg" ${item.unit === 'kg' ? 'selected' : ''}>Kilograms (kg)</option>
                            <option value="g" ${item.unit === 'g' ? 'selected' : ''}>Grams (g)</option>
                        </select>
                    </div>
                    
                    <div style="display:flex; justify-content: space-between; align-items: flex-end; margin-top: auto;">
                        <span class="remove-item" onclick="removeFromCart(${item.id})"><i class="fa-solid fa-trash-can"></i> Delete</span>
                        <div class="cart-subtotal">₹${itemTotal.toFixed(2)}</div>
                    </div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
    document.getElementById('cartTotal').innerText = '₹' + grandTotal.toFixed(2);
}

function renderOrders() {
    const container = document.getElementById('cartOrdersContainer');
    if (!container) return;
    
    if (orders.length === 0) {
        container.innerHTML = '<div style="text-align:center; padding: 50px 20px; color:#6b7280;">No active orders found.</div>';
        return;
    }
    
    let html = '';
    orders.forEach(order => {
        let itemsHtml = order.items.map(i => `
            <div style="display:flex; justify-content: space-between; font-size: 0.9rem; margin-top: 8px; color: #374151;">
                <span>${i.qty} ${i.unit} x ${i.title}</span>
                <span>₹${calculateItemTotal(i.basePrice, i.qty, i.unit).toFixed(2)}</span>
            </div>
        `).join('');
        
        html += `
            <div class="order-card">
                <div class="order-header">
                    <div>
                        <div class="order-id">Order #${order.id}</div>
                        <div class="order-date">Placed on ${order.date}</div>
                    </div>
                    <div>
                        <span class="order-status">${order.status}</span>
                    </div>
                </div>
                <div style="margin-bottom: 12px;">
                    ${itemsHtml}
                </div>
                <div style="border-top: 1px dashed #d1d5db; padding-top: 12px; display: flex; justify-content: space-between; font-weight: bold; font-size: 1.1rem;">
                    <span>Order Total:</span>
                    <span>₹${order.total.toFixed(2)}</span>
                </div>
            </div>
        `;
    });
    container.innerHTML = html;
}

function checkoutCart() {
    if (cart.length === 0) return;
    
    let total = 0;
    cart.forEach(item => {
        total += calculateItemTotal(item.basePrice, item.qty, item.unit);
    });
    
    const newOrder = {
        id: Math.floor(100000 + Math.random() * 900000),
        items: [...cart],
        total: total,
        status: 'Processing',
        date: new Date().toLocaleString()
    };
    
    orders.unshift(newOrder);
    localStorage.setItem('agriOrders', JSON.stringify(orders));
    
    cart = [];
    localStorage.setItem(getCartKey(), JSON.stringify(cart));
    
    updateCartBadge();
    switchCartTab('orders');
    renderOrders();
    showToast('Order placed successfully!', 'success');
}
