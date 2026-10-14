import glob

def upgrade_templates():
    html_files = glob.glob('templates/**/*.html', recursive=True)
    
    # 1. Update image src in all files
    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Replace the url_for static image logic with conditional
        # to support the new http Unsplash links
        old_img_src = '{{ url_for(\'static\', filename=prod.image_url) }}'
        new_img_src = '{% if prod.image_url and prod.image_url.startswith("http") %}{{ prod.image_url }}{% else %}{{ url_for(\'static\', filename=prod.image_url) }}{% endif %}'
        content = content.replace(old_img_src, new_img_src)
        
        old_img_src2 = '{{ url_for(\'static\', filename=product.image_url) }}'
        new_img_src2 = '{% if product.image_url and product.image_url.startswith("http") %}{{ product.image_url }}{% else %}{{ url_for(\'static\', filename=product.image_url) }}{% endif %}'
        content = content.replace(old_img_src2, new_img_src2)
        
        old_img_src3 = '{{ url_for(\'static\', filename=item.product.image_url) }}'
        new_img_src3 = '{% if item.product.image_url and item.product.image_url.startswith("http") %}{{ item.product.image_url }}{% else %}{{ url_for(\'static\', filename=item.product.image_url) }}{% endif %}'
        content = content.replace(old_img_src3, new_img_src3)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
    print("Updated all image links to support HTTP urls.")
    
    # 2. Make base.html extremely aesthetic
    base_html_path = 'templates/base.html'
    with open(base_html_path, 'r', encoding='utf-8') as f:
        base_content = f.read()
        
    # Replace bootstrap with Bootswatch Zephyr and add custom CSS
    old_head = '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">'
    new_head = '''<link href="https://cdn.jsdelivr.net/npm/bootswatch@5.3.0/zephyr/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { font-family: 'Poppins', sans-serif; background-color: #f4f7f6; }
        .navbar { box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        .product-card { 
            border: none; 
            border-radius: 16px; 
            overflow: hidden;
            box-shadow: 0 8px 24px rgba(0,0,0,0.04);
            transition: all 0.3s ease; 
            background: #fff;
        }
        .product-card:hover { 
            transform: translateY(-8px); 
            box-shadow: 0 16px 32px rgba(0,0,0,0.1); 
        }
        .product-card .card-img-top {
            border-bottom: 1px solid #f0f0f0;
        }
        .btn-primary { border-radius: 8px; font-weight: 500; }
        .explanation-box { 
            display: none; margin-top: 10px; padding: 15px; 
            background-color: #e9f5ff; border-radius: 8px; 
            border-left: 4px solid #0d6efd; font-size: 0.9em; 
        }
        .badge { font-weight: 500; }
        footer { background: #fff; box-shadow: 0 -4px 12px rgba(0,0,0,0.02); }
        h1, h2, h3, h4, h5 { font-weight: 600; }
    </style>'''
    
    base_content = base_content.replace(old_head, new_head)
    
    # Optional: Make navbar icons
    base_content = base_content.replace('Cart <span', '<i class="fas fa-shopping-cart"></i> Cart <span')
    base_content = base_content.replace('Personalized Recommendations ✨', '<i class="fas fa-magic text-warning"></i> AI Recommendations')
    
    with open(base_html_path, 'w', encoding='utf-8') as f:
        f.write(base_content)
        
    print("Upgraded base.html to a highly aesthetic modern theme.")

if __name__ == '__main__':
    upgrade_templates()
