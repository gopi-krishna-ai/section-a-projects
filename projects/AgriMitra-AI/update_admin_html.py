import re

new_admin_html = """{% extends "base.html" %}

{% block title %}Admin Panel - AgriMitra AI{% endblock %}

{% block content %}
<style>
    .admin-tabs { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px; }
    .admin-tab { padding: 10px 20px; background: none; border: none; font-size: 16px; font-weight: bold; color: #6b7280; cursor: pointer; transition: all 0.2s; border-radius: 6px; }
    .admin-tab:hover { background: #f3f4f6; color: #111; }
    .admin-tab.active { background: #166534; color: white; }
    .admin-section { display: none; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .admin-section.active { display: block; }
    .data-table { width: 100%; border-collapse: collapse; margin-top: 15px; }
    .data-table th, .data-table td { border: 1px solid #e5e7eb; padding: 12px; text-align: left; font-size: 14px; }
    .data-table th { background: #f9fafb; font-weight: bold; }
    .btn-sm { padding: 5px 10px; border-radius: 4px; font-size: 12px; border: none; cursor: pointer; color: white; }
    .btn-edit { background: #0284c7; }
    .btn-del { background: #ef4444; }
    .btn-action { background: #ca8a04; }
</style>

<section class="main-content" style="padding: 20px;">
    <h1 style="margin-bottom: 20px;"><i class="fa-solid fa-chart-pie"></i> Admin Control Center</h1>
    
    <div class="admin-tabs">
        <button class="admin-tab active" onclick="switchTab('upload')"><i class="fa-solid fa-upload"></i> Upload</button>
        <button class="admin-tab" onclick="switchTab('manage')"><i class="fa-solid fa-box"></i> Manage Products</button>
        <button class="admin-tab" onclick="switchTab('orders')"><i class="fa-solid fa-truck"></i> Orders</button>
        <button class="admin-tab" onclick="switchTab('users')"><i class="fa-solid fa-users"></i> Users</button>
    </div>

    <!-- UPLOAD TAB -->
    <div id="tab-upload" class="admin-section active" style="max-width: 600px;">
        <h3>Add New Product</h3>
        <form id="adminForm" onsubmit="submitProduct(event)">
            <div style="margin-bottom: 15px;">
                <label style="display:block; font-weight:bold; margin-bottom:5px;">Product Type</label>
                <select id="item_type" name="item_type" style="width:100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px;" required>
                    <option value="seed">Seed</option>
                    <option value="fertilizer">Fertilizer</option>
                </select>
            </div>
            <div style="margin-bottom: 15px;">
                <label style="display:block; font-weight:bold; margin-bottom:5px;">Item Name (e.g. "Coffee")</label>
                <input type="text" id="item_name" name="item_name" style="width:100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px;" required>
            </div>
            <div style="margin-bottom: 15px;">
                <label style="display:block; font-weight:bold; margin-bottom:5px;">Seller Name</label>
                <input type="text" id="seller" name="seller" style="width:100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px;" required>
            </div>
            <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                <div style="flex:1;">
                    <label style="display:block; font-weight:bold; margin-bottom:5px;">Price (per kg)</label>
                    <input type="number" step="0.01" id="price" name="price" style="width:100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px;" required>
                </div>
                <div style="flex:1;">
                    <label style="display:block; font-weight:bold; margin-bottom:5px;">Stock (kg)</label>
                    <input type="number" id="stock" name="stock" value="100" style="width:100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px;" required>
                </div>
                <div style="flex:1;">
                    <label style="display:block; font-weight:bold; margin-bottom:5px;">Discount (%)</label>
                    <input type="number" id="discount" name="discount" value="0" style="width:100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">
                </div>
            </div>
            <div style="margin-bottom: 15px;">
                <label style="display:block; font-weight:bold; margin-bottom:5px;">Description</label>
                <textarea id="description" name="description" rows="3" style="width:100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px;" required></textarea>
            </div>
            <div style="margin-bottom: 20px;">
                <label style="display:block; font-weight:bold; margin-bottom:5px;">Product Image</label>
                <input type="file" id="image" name="image" accept="image/*" style="width:100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">
            </div>
            <button type="submit" style="background: var(--c-primary); color: white; border: none; padding: 12px 20px; font-size: 1rem; font-weight: bold; border-radius: 6px; cursor: pointer; width: 100%;">Upload Product</button>
        </form>
    </div>

    <!-- MANAGE TAB -->
    <div id="tab-manage" class="admin-section">
        <h3>Manage Inventory</h3>
        <table class="data-table" id="productsTable">
            <thead>
                <tr>
                    <th>Img</th><th>Name</th><th>Type</th><th>Price</th><th>Stock</th><th>Discount</th><th>Actions</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>
    </div>

    <!-- ORDERS TAB -->
    <div id="tab-orders" class="admin-section">
        <h3>Recent Orders</h3>
        <table class="data-table" id="ordersTable">
            <thead>
                <tr>
                    <th>Order #</th><th>Date</th><th>Customer</th><th>Items</th><th>Total</th><th>Status</th><th>Actions</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>
    </div>

    <!-- USERS TAB -->
    <div id="tab-users" class="admin-section">
        <h3>Registered Farmers</h3>
        <table class="data-table" id="usersTable">
            <thead>
                <tr>
                    <th>ID</th><th>Name</th><th>User ID</th><th>Email</th><th>Phone</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>
    </div>

</section>
{% endblock %}

{% block scripts %}
<script>
function switchTab(tabId) {
    document.querySelectorAll('.admin-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.admin-section').forEach(s => s.classList.remove('active'));
    
    event.currentTarget.classList.add('active');
    document.getElementById('tab-' + tabId).classList.add('active');

    if (tabId === 'manage') loadProducts();
    if (tabId === 'orders') loadOrders();
    if (tabId === 'users') loadUsers();
}

async function submitProduct(e) {
    e.preventDefault();
    const form = document.getElementById('adminForm');
    const formData = new FormData(form);
    try {
        const res = await fetch('/api/admin/product', { method: 'POST', body: formData });
        const data = await res.json();
        if (data.success) { showToast(data.message, 'success'); form.reset(); }
        else { showToast("Error: " + data.message, 'error'); }
    } catch(err) { showToast("Upload failed.", 'error'); }
}

async function loadProducts() {
    const res = await fetch('/api/products');
    const data = await res.json();
    const tbody = document.querySelector('#productsTable tbody');
    tbody.innerHTML = data.map(p => `
        <tr>
            <td><img src="${p.image_url}" width="40" height="40" style="border-radius:4px; object-fit:cover;"></td>
            <td>${p.item_name}<br><small>${p.seller}</small></td>
            <td>${p.item_type}</td>
            <td>₹${p.price.toFixed(2)}</td>
            <td>${p.stock} kg</td>
            <td>${p.discount}%</td>
            <td>
                <button class="btn-sm btn-del" onclick="deleteProduct(${p.id})"><i class="fa-solid fa-trash"></i></button>
            </td>
        </tr>
    `).join('');
}

async function deleteProduct(id) {
    if(!confirm("Delete this product?")) return;
    await fetch(`/api/admin/product/${id}`, { method: 'DELETE' });
    loadProducts();
}

async function loadOrders() {
    const res = await fetch('/api/admin/orders');
    const data = await res.json();
    const tbody = document.querySelector('#ordersTable tbody');
    tbody.innerHTML = data.orders.map(o => `
        <tr>
            <td>#${o.id}</td>
            <td>${o.created_at}</td>
            <td>${o.user}<br><small>${o.email}</small></td>
            <td>${o.items.map(i => `${i.quantity}kg ${i.product_name}`).join('<br>')}</td>
            <td>₹${o.total_amount.toFixed(2)}</td>
            <td><span style="padding:3px 8px; border-radius:12px; background:${o.status==='Pending'?'#fef08a':(o.status==='Shipped'?'#bae6fd':'#bbf7d0')}; color:#111; font-size:12px;">${o.status}</span></td>
            <td>
                <select onchange="updateOrderStatus(${o.id}, this.value)" style="padding:4px; border-radius:4px;">
                    <option value="" disabled selected>Update</option>
                    <option value="Pending">Pending</option>
                    <option value="Shipped">Shipped</option>
                    <option value="Delivered">Delivered</option>
                </select>
            </td>
        </tr>
    `).join('');
}

async function updateOrderStatus(id, status) {
    await fetch(`/api/admin/orders/${id}/status`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({status})
    });
    loadOrders();
}

async function loadUsers() {
    const res = await fetch('/api/admin/users');
    const data = await res.json();
    const tbody = document.querySelector('#usersTable tbody');
    tbody.innerHTML = data.users.map(u => `
        <tr>
            <td>${u.id}</td>
            <td>${u.fullname}</td>
            <td>${u.userid}</td>
            <td>${u.email}</td>
            <td>${u.phone}</td>
        </tr>
    `).join('');
}
</script>
{% endblock %}
"""

with open('templates/admin.html', 'w', encoding='utf-8') as f:
    f.write(new_admin_html)

print("Updated admin.html with tabs for features")
