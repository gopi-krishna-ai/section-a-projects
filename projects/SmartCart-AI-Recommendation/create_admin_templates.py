import os

def create_admin_templates():
    admin_login = """{% extends "base.html" %}
{% block content %}
<div class="row justify-content-center mt-5">
    <div class="col-md-5">
        <div class="card product-card p-4">
            <h3 class="text-center mb-4"><i class="fas fa-user-shield text-danger"></i> Admin Login</h3>
            <form action="{{ url_for('admin_login') }}" method="POST">
                <div class="mb-3">
                    <label class="form-label fw-bold">Admin Username</label>
                    <input type="text" class="form-control" name="username" required value="admin">
                </div>
                <div class="mb-4">
                    <label class="form-label fw-bold">Password</label>
                    <input type="password" class="form-control" name="password" required value="admin123">
                </div>
                <button type="submit" class="btn btn-danger w-100 py-2 fw-bold">Login to Admin Panel</button>
            </form>
        </div>
    </div>
</div>
{% endblock %}
"""
    with open('templates/admin_login.html', 'w', encoding='utf-8') as f:
        f.write(admin_login)

    admin_dashboard = """{% extends "base.html" %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4 mt-4">
    <h2 class="fw-bold"><i class="fas fa-cogs"></i> Admin Dashboard</h2>
    <div>
        <a href="{{ url_for('admin_add_product') }}" class="btn btn-primary"><i class="fas fa-plus"></i> Add New Product</a>
        <a href="{{ url_for('admin_logout') }}" class="btn btn-outline-danger ms-2"><i class="fas fa-sign-out-alt"></i> Logout</a>
    </div>
</div>

<div class="card product-card p-4">
    <h4 class="mb-4">Product Management</h4>
    <div class="table-responsive">
        <table class="table table-hover align-middle">
            <thead class="table-light">
                <tr>
                    <th>Image</th>
                    <th>Name</th>
                    <th>Category</th>
                    <th>Price</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for prod in products %}
                <tr>
                    <td>
                        <img src="{% if prod.image_url and prod.image_url.startswith('http') %}{{ prod.image_url }}{% else %}{{ url_for('static', filename=prod.image_url) }}{% endif %}" alt="{{ prod.name }}" class="rounded" style="width: 50px; height: 50px; object-fit: cover;">
                    </td>
                    <td class="fw-bold">{{ prod.name }}</td>
                    <td><span class="badge bg-secondary">{{ prod.category.name }}</span></td>
                    <td class="text-success fw-bold">${{ "%.2f"|format(prod.price) }}</td>
                    <td>
                        <a href="{{ url_for('admin_edit_product', product_id=prod.id) }}" class="btn btn-sm btn-warning"><i class="fas fa-edit"></i> Edit Photo & Details</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
"""
    with open('templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(admin_dashboard)

    admin_add_product = """{% extends "base.html" %}
{% block content %}
<div class="row justify-content-center mt-4">
    <div class="col-md-8">
        <div class="card product-card p-4">
            <div class="d-flex justify-content-between mb-4">
                <h3 class="fw-bold"><i class="fas fa-plus-circle text-primary"></i> Add New Product</h3>
                <a href="{{ url_for('admin_dashboard') }}" class="btn btn-outline-secondary">Back to Dashboard</a>
            </div>
            
            <form action="{{ url_for('admin_add_product') }}" method="POST" enctype="multipart/form-data">
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label class="form-label fw-bold">Product Name</label>
                        <input type="text" class="form-control" name="name" required>
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label fw-bold">Category</label>
                        <select class="form-select" name="category_id" required>
                            {% for cat in categories %}
                            <option value="{{ cat.id }}">{{ cat.name }}</option>
                            {% endfor %}
                        </select>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label class="form-label fw-bold">Price ($)</label>
                        <input type="number" step="0.01" class="form-control" name="price" required>
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label fw-bold">Product Image (Upload Photo)</label>
                        <input type="file" class="form-control" name="image" accept="image/*" required>
                    </div>
                </div>
                
                <div class="mb-4">
                    <label class="form-label fw-bold">Description</label>
                    <textarea class="form-control" name="description" rows="3" required></textarea>
                </div>
                
                <button type="submit" class="btn btn-primary w-100 py-2 fw-bold">Save New Product</button>
            </form>
        </div>
    </div>
</div>
{% endblock %}
"""
    with open('templates/admin_add_product.html', 'w', encoding='utf-8') as f:
        f.write(admin_add_product)

    admin_edit_product = """{% extends "base.html" %}
{% block content %}
<div class="row justify-content-center mt-4">
    <div class="col-md-8">
        <div class="card product-card p-4">
            <div class="d-flex justify-content-between mb-4">
                <h3 class="fw-bold"><i class="fas fa-edit text-warning"></i> Edit Product & Photo</h3>
                <a href="{{ url_for('admin_dashboard') }}" class="btn btn-outline-secondary">Back to Dashboard</a>
            </div>
            
            <div class="text-center mb-4">
                <img src="{% if product.image_url and product.image_url.startswith('http') %}{{ product.image_url }}{% else %}{{ url_for('static', filename=product.image_url) }}{% endif %}" class="rounded shadow-sm" style="height: 150px; object-fit: cover;">
                <p class="text-muted small mt-2">Current Photo</p>
            </div>
            
            <form action="{{ url_for('admin_edit_product', product_id=product.id) }}" method="POST" enctype="multipart/form-data">
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label class="form-label fw-bold">Product Name</label>
                        <input type="text" class="form-control" name="name" value="{{ product.name }}" required>
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label fw-bold">Category</label>
                        <select class="form-select" name="category_id" required>
                            {% for cat in categories %}
                            <option value="{{ cat.id }}" {% if cat.id == product.category_id %}selected{% endif %}>{{ cat.name }}</option>
                            {% endfor %}
                        </select>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label class="form-label fw-bold">Price ($)</label>
                        <input type="number" step="0.01" class="form-control" name="price" value="{{ product.price }}" required>
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label fw-bold text-primary">Upload NEW Photo (Optional)</label>
                        <input type="file" class="form-control border-primary" name="image" accept="image/*">
                        <small class="text-muted">Leave blank to keep the current photo.</small>
                    </div>
                </div>
                
                <div class="mb-4">
                    <label class="form-label fw-bold">Description</label>
                    <textarea class="form-control" name="description" rows="3" required>{{ product.description }}</textarea>
                </div>
                
                <button type="submit" class="btn btn-warning w-100 py-2 fw-bold text-dark">Update Product & Photo</button>
            </form>
        </div>
    </div>
</div>
{% endblock %}
"""
    with open('templates/admin_edit_product.html', 'w', encoding='utf-8') as f:
        f.write(admin_edit_product)
        
    print("Admin templates created successfully!")

if __name__ == '__main__':
    create_admin_templates()
