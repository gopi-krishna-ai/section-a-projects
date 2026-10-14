import os
import glob

def upgrade_rest():
    shop_html = """{% extends "base.html" %}

{% block content %}
<div class="row align-items-center mb-4 mt-3">
    <div class="col-md-8">
        <h2 class="fw-bold m-0" style="color: #111827;">Explore Collection</h2>
        {% if query %}
            <p class="text-muted mt-2">Showing search results for "<span class="fw-bold text-dark">{{ query }}</span>"</p>
        {% endif %}
    </div>
</div>

<div class="row">
    <div class="col-md-3 mb-4">
        <div class="card border-0 shadow-sm rounded-4 p-3" style="background: white;">
            <h5 class="fw-bold mb-3 px-2">Categories</h5>
            <div class="list-group list-group-flush border-0">
                <a href="{{ url_for('shop') }}" class="list-group-item list-group-item-action border-0 rounded-3 mb-1 {% if not request.args.get('category') %}active bg-primary text-white{% endif %}">
                    <i class="fas fa-th-large me-2"></i> All Categories
                </a>
                {% for cat in categories %}
                    <a href="{{ url_for('shop', category=cat.id) }}" class="list-group-item list-group-item-action border-0 rounded-3 mb-1 {% if request.args.get('category')|string == cat.id|string %}active bg-primary text-white{% endif %}">
                        {{ cat.name }}
                    </a>
                {% endfor %}
            </div>
        </div>
    </div>
    
    <div class="col-md-9">
        {% if products %}
            <div class="row row-cols-1 row-cols-md-3 g-4">
                {% for prod in products %}
                <div class="col">
                    <div class="card product-card h-100">
                        <div class="img-wrapper">
                            <img src="{% if prod.image_url and prod.image_url.startswith('http') %}{{ prod.image_url }}{% else %}{{ url_for('static', filename=prod.image_url) }}{% endif %}" class="card-img-top w-100" alt="{{ prod.name }}">
                        </div>
                        <div class="card-body d-flex flex-column">
                            <p class="text-muted small fw-semibold text-uppercase tracking-wider mb-1">{{ prod.category.name }}</p>
                            <h5 class="card-title text-truncate">{{ prod.name }}</h5>
                            <div class="star-rating mb-2">
                                <i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star-half-alt"></i>
                            </div>
                            <div class="mt-auto d-flex justify-content-between align-items-center">
                                <h6 class="card-price m-0">${{ "%.2f"|format(prod.price) }}</h6>
                                <a href="{{ url_for('product', product_id=prod.id) }}" class="btn btn-dark rounded-circle" style="width: 40px; height: 40px; padding: 8px;"><i class="fas fa-plus"></i></a>
                            </div>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        {% else %}
            <div class="text-center p-5 bg-white rounded-4 shadow-sm border-0 mt-4">
                <i class="fas fa-box-open fa-4x text-muted mb-3 opacity-50"></i>
                <h4 class="fw-bold">No Products Found</h4>
                <p class="text-muted">Try adjusting your search or filter criteria.</p>
                <a href="{{ url_for('shop') }}" class="btn btn-outline-primary mt-2 rounded-pill px-4">Clear Filters</a>
            </div>
        {% endif %}
    </div>
</div>
{% endblock %}"""
    with open('templates/shop.html', 'w', encoding='utf-8') as f:
        f.write(shop_html)

    recs_html = """{% extends "base.html" %}

{% block content %}
<div class="row mb-5 mt-4">
    <div class="col-md-12 text-center">
        <span class="badge bg-warning text-dark px-3 py-2 rounded-pill mb-3 fw-bold shadow-sm" style="font-size: 0.9rem;"><i class="fas fa-magic me-1"></i> AI Curated For You</span>
        <h2 class="fw-bold" style="font-size: 2.5rem; letter-spacing: -1px;">Your Personalized Feed</h2>
        <p class="text-muted fs-5">Powered by Random Forest Machine Learning</p>
    </div>
</div>

<div class="row row-cols-1 row-cols-md-4 g-4 mt-2">
    {% for prod in recommendations %}
    <div class="col">
        <div class="card product-card h-100">
            <div class="img-wrapper">
                <span class="badge-premium bg-warning text-dark border border-warning shadow-sm" style="top: 10px; right: 10px; left: auto;"><i class="fas fa-bolt"></i> 99% Match</span>
                <img src="{% if prod.image_url and prod.image_url.startswith('http') %}{{ prod.image_url }}{% else %}{{ url_for('static', filename=prod.image_url) }}{% endif %}" class="card-img-top w-100" alt="{{ prod.name }}">
            </div>
            <div class="card-body d-flex flex-column">
                <p class="text-muted small fw-semibold text-uppercase tracking-wider mb-1">{{ prod.category.name }}</p>
                <h5 class="card-title text-truncate">{{ prod.name }}</h5>
                <div class="star-rating mb-2">
                    <i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i>
                </div>
                
                <div class="mt-3 p-3 bg-light rounded-3 border-start border-4 border-warning small">
                    <strong><i class="fas fa-robot text-muted"></i> Why this?</strong><br>
                    <span class="text-muted">{{ explanations[prod.id] }}</span>
                </div>
                
                <div class="mt-auto pt-3 d-flex justify-content-between align-items-center">
                    <h6 class="card-price m-0">${{ "%.2f"|format(prod.price) }}</h6>
                    <a href="{{ url_for('product', product_id=prod.id) }}" class="btn btn-primary rounded-pill px-4">View</a>
                </div>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}"""
    with open('templates/recommendations.html', 'w', encoding='utf-8') as f:
        f.write(recs_html)
        
    print("Done upgrading shop and recommendations!")

if __name__ == '__main__':
    upgrade_rest()
