import os

def fix_indentation():
    with open('backend/routes.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    with open('backend/routes.py', 'w', encoding='utf-8') as f:
        for line in lines:
            if line.startswith("        @app.route('/add_to_cart/"):
                f.write("    " + line.strip() + "\n")
            elif line.startswith("        @app.route('/remove_from_cart/"):
                f.write("    " + line.strip() + "\n")
            elif line.startswith("        @app.route('/cart')"):
                f.write("    " + line.strip() + "\n")
            elif line.startswith("        @app.route('/checkout',"):
                f.write("    " + line.strip() + "\n")
            else:
                f.write(line)
                
    print("Indentation fixed!")

if __name__ == '__main__':
    fix_indentation()
