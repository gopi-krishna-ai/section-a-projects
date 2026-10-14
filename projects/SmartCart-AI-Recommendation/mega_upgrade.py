import os
import glob

def mega_upgrade():
    # 1. UPGRADE BASE.HTML
    base_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartCart - Premium AI Shopping</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #4F46E5;
            --primary-hover: #4338CA;
            --surface: #ffffff;
            --background: #F3F4F6;
            --text-main: #111827;
            --text-muted: #6B7280;
        }
        body { 
            font-family: 'Plus Jakarta Sans', sans-serif; 
            background-color: var(--background); 
            color: var(--text-main);
            padding-top: 80px;
        }
        /* Glassmorphism Navbar */
        .navbar {
            background: rgba(255, 255, 255, 0.8) !important;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(255,255,255,0.3);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
            padding: 15px 0;
            position: fixed;
            top: 0; width: 100%; z-index: 1000;
        }
        .navbar-brand { font-weight: 800; font-size: 1.5rem; color: var(--primary) !important; }
        .nav-link { font-weight: 600; color: var(--text-main) !important; transition: all 0.2s; }
        .nav-link:hover { color: var(--primary) !important; transform: translateY(-1px); }
        .btn-primary { background-color: var(--primary); border: none; border-radius: 10px; font-weight: 600; padding: 10px 24px; box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3); transition: all 0.3s; }
        .btn-primary:hover { background-color: var(--primary-hover); transform: translateY(-2px); box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4); }
        .btn-outline-primary { border-color: var(--primary); color: var(--primary); border-radius: 10px; font-weight: 600; }
        .btn-outline-primary:hover { background-color: var(--primary); color: white; }
        
        /* Premium Product Cards */
        .product-card { 
            border: 1px solid rgba(0,0,0,0.04); 
            border-radius: 20px; 
            overflow: hidden;
            background: var(--surface);
            box-shadow: 0 10px 25px rgba(0,0,0,0.03);
            transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            position: relative;
        }
        .product-card:hover { 
            transform: translateY(-8px) scale(1.01); 
            box-shadow: 0 20px 40px rgba(0,0,0,0.08); 
        }
        .card-img-top {
            height: 220px;
            object-fit: cover;
            border-bottom: 1px solid rgba(0,0,0,0.03);
            transition: transform 0.5s ease;
        }
        .product-card:hover .card-img-top { transform: scale(1.05); }
        .img-wrapper { overflow: hidden; position: relative; }
        .badge-premium { position: absolute; top: 15px; left: 15px; background: rgba(255,255,255,0.9); backdrop-filter: blur(4px); color: var(--primary); font-weight: 700; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1); z-index: 10; }
        
        .card-body { padding: 24px; }
        .card-title { font-weight: 700; font-size: 1.1rem; margin-bottom: 8px; }
        .card-price { font-weight: 800; font-size: 1.3rem; color: var(--primary); }
        
        .star-rating { color: #F59E0B; font-size: 0.9rem; }
        
        /* Hero Section */
        .hero-banner {
            background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
            border-radius: 30px;
            padding: 80px 40px;
            text-align: center;
            box-shadow: 0 20px 40px rgba(79, 70, 229, 0.1);
            margin-bottom: 60px;
            position: relative;
            overflow: hidden;
        }
        .hero-banner::before { content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 70%); animation: rotate 20s linear infinite; }
        @keyframes rotate { 100% { transform: rotate(360deg); } }
        .hero-title { font-weight: 800; font-size: 3.5rem; color: #1E3A8A; position: relative; z-index: 1; letter-spacing: -1px; }
        .hero-subtitle { font-size: 1.2rem; color: #4F46E5; font-weight: 500; margin-bottom: 30px; position: relative; z-index: 1; }
        
        footer { background: #ffffff; padding: 40px 0; margin-top: 80px; border-top: 1px solid rgba(0,0,0,0.05); }
    </style>
</head>
<body>

<nav class="navbar navbar-expand-lg">
  <div class="container">
    <a class="navbar-brand" href="{{ url_for('index') }}"><i class="fas fa-shopping-bag me-2"></i>SmartCart</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav me-auto">
        <li class="nav-item"><a class="nav-link" href="{{ url_for('index') }}">Home</a></li>
        <li class="nav-item"><a class="nav-link" href="{{ url_for('shop') }}">Shop</a></li>
        <li class="nav-item"><a class="nav-link" href="{{ url_for('recommendations') }}" style="color: #F59E0B !important;"><i class="fas fa-sparkles"></i> AI Recommendations</a></li>
      </ul>
      
      <form class="d-flex me-4" action="{{ url_for('shop') }}" method="GET">
        <div class="input-group">
            <span class="input-group-text bg-white border-end-0 rounded-start-pill text-muted"><i class="fas fa-search"></i></span>
            <input class="form-control border-start-0 rounded-end-pill" type="search" name="q" placeholder="Search premium products..." style="box-shadow: none; border-color: #dee2e6;">
        </div>
      </form>

      <ul class="navbar-nav align-items-center">
        <li class="nav-item me-3">
          <a class="nav-link position-relative" href="{{ url_for('cart') }}">
            <i class="fas fa-shopping-cart fa-lg"></i>
            <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" style="font-size: 0.6rem;">{{ cart_count }}</span>
          </a>
        </li>
        {% if session.customer_id %}
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle fw-bold" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown">
            <img src="https://ui-avatars.com/api/?name={{ session.customer_name }}&background=4F46E5&color=fff&rounded=true" alt="User" width="32" height="32" class="me-1">
            {{ session.customer_name }}
          </a>
          <ul class="dropdown-menu dropdown-menu-end border-0 shadow-lg" style="border-radius: 15px;">
            <li><a class="dropdown-item py-2" href="{{ url_for('profile') }}"><i class="fas fa-user me-2 text-muted"></i> Profile</a></li>
            <li><a class="dropdown-item py-2" href="{{ url_for('orders') }}"><i class="fas fa-box me-2 text-muted"></i> My Orders</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item py-2 text-danger" href="{{ url_for('logout') }}"><i class="fas fa-sign-out-alt me-2"></i> Logout</a></li>
          </ul>
        </li>
        {% else %}
        <li class="nav-item"><a class="btn btn-primary px-4 rounded-pill" href="{{ url_for('login') }}">Sign In</a></li>
        {% endif %}
      </ul>
    </div>
  </div>
</nav>

<div class="container" style="min-height: 70vh;">
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        <div class="mt-4">
        {% for category, message in messages %}
          <div class="alert alert-{{ category }} alert-dismissible fade show rounded-4 border-0 shadow-sm" role="alert">
            <i class="fas fa-info-circle me-2"></i> {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
          </div>
        {% endfor %}
        </div>
      {% endif %}
    {% endwith %}

    {% block content %}{% endblock %}
</div>

<footer class="text-center text-muted">
  <div class="container">
    <p class="mb-0 fw-medium">© 2026 SmartCart. Powered by Advanced Machine Learning.</p>
  </div>
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(base_html)

    # 2. UPGRADE INDEX.HTML
    index_html = """{% extends "base.html" %}

{% block content %}
<div class="hero-banner">
    <h1 class="hero-title">Shopping, Reimagined.</h1>
    <p class="hero-subtitle">Our Random Forest AI learns your style to curate the perfect feed.</p>
    <a href="{{ url_for('shop') }}" class="btn btn-primary btn-lg rounded-pill px-5 py-3 shadow-lg fs-5">Explore Collection <i class="fas fa-arrow-right ms-2"></i></a>
</div>

<div class="row mb-5 mt-5">
    <div class="col-md-12">
        <div class="d-flex justify-content-between align-items-end mb-4">
            <h3 class="fw-bold m-0" style="color: #111827;">Trending Now</h3>
            <a href="{{ url_for('shop') }}" class="text-decoration-none fw-semibold" style="color: var(--primary);">View All <i class="fas fa-chevron-right ms-1"></i></a>
        </div>
        <div class="row row-cols-1 row-cols-md-4 g-4">
            {% for prod in trending %}
            <div class="col">
                <div class="card product-card h-100">
                    <div class="img-wrapper">
                        <span class="badge-premium"><i class="fas fa-fire text-danger"></i> Hot</span>
                        <img src="{% if prod.image_url and prod.image_url.startswith('http') %}{{ prod.image_url }}{% else %}{{ url_for('static', filename=prod.image_url) }}{% endif %}" class="card-img-top w-100" alt="{{ prod.name }}">
                    </div>
                    <div class="card-body d-flex flex-column">
                        <p class="text-muted small fw-semibold text-uppercase tracking-wider mb-1">{{ prod.category.name }}</p>
                        <h5 class="card-title text-truncate">{{ prod.name }}</h5>
                        <div class="star-rating mb-2">
                            <i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star-half-alt"></i>
                            <span class="text-muted small ms-1">({{ prod.review_count }})</span>
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
    </div>
</div>

<div class="row mb-5">
    <div class="col-md-12 text-center">
        <h3 class="fw-bold mb-4">Shop by Category</h3>
        <div class="d-flex flex-wrap justify-content-center gap-3">
            {% for cat in categories %}
                <a href="{{ url_for('shop', category=cat.id) }}" class="btn btn-outline-secondary rounded-pill px-4 py-2 fw-medium shadow-sm hover-lift">{{ cat.name }}</a>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}"""
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
        
    print("Mega upgrade complete!")

if __name__ == '__main__':
    mega_upgrade()
