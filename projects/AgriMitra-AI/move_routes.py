import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract admin routes using simpler matching
admin_match = re.search(r'(@app\.route\("/admin"\).*?)(?=@app\.route)', content, re.DOTALL)
product_match = re.search(r'(@app\.route\("/api/admin/product", methods=\["POST"\]\).*?)(?=@app\.route)', content, re.DOTALL)

if admin_match and product_match:
    admin_code = admin_match.group(1)
    product_code = product_match.group(1)
    
    # Remove from current location
    content = content.replace(admin_code, '')
    content = content.replace(product_code, '')
    
    # Insert before main
    content = content.replace('if __name__ == "__main__":', admin_code + '\n' + product_code + '\nif __name__ == "__main__":')
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Routes moved successfully.")
else:
    print("Could not find routes to move.")
