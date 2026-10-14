import os

def update_plus_buttons():
    files = ['templates/shop.html', 'templates/index.html', 'templates/recommendations.html']
    
    old_btn = '<a href="{{ url_for(\'product\', product_id=prod.id) }}" class="btn btn-dark rounded-circle shadow-sm" style="width: 40px; height: 40px; padding: 8px;"><i class="fas fa-plus"></i></a>'
    
    new_btn = """<form action="{{ url_for('add_to_cart', product_id=prod.id) }}" method="POST" class="d-inline">
            <button type="submit" class="btn btn-dark rounded-circle shadow-sm" style="width: 40px; height: 40px; padding: 8px;" title="Add to Cart">
                <i class="fas fa-plus"></i>
            </button>
        </form>"""
        
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        content = content.replace(old_btn, new_btn)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
            
    print("Updated all + buttons to direct Add to Cart!")

if __name__ == '__main__':
    update_plus_buttons()
