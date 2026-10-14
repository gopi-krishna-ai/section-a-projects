import os

def inject_crop():
    with open('templates/crop.html', 'r', encoding='utf-8') as f:
        html = f.read()

    ecart_html = '''
    <!-- E-Commerce Section -->
    <div class="result-card" id="ecartSection" style="margin-top: 20px; background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border: 2px solid #22c55e;">
        <h4 style="color: #166534; font-weight: bold; margin-bottom: 15px;"><i class="fa-solid fa-store"></i> Buy Premium Seeds</h4>
        <div style="display: flex; gap: 15px; flex-wrap: wrap; align-items: center;">
            <div style="flex: 0 0 120px; height: 120px; border-radius: 10px; overflow: hidden; background: white; border: 1px solid #bbf7d0; display: flex; justify-content: center; align-items: center;">
                <img id="ecartImg" src="" alt="Seeds" style="max-width: 100%; max-height: 100%; object-fit: cover;">
            </div>
            <div style="flex: 1; min-width: 200px;">
                <h5 id="ecartTitle" style="margin-bottom: 5px; font-weight: 600; font-size: 1.1rem; color: #15803d;"></h5>
                <p id="ecartDesc" style="font-size: 0.9rem; color: #166534; margin-bottom: 10px;">High-yield, disease-resistant seeds tailored for your soil.</p>
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                    <span style="text-decoration: line-through; color: #ef4444; font-size: 0.9rem;">₹<span id="ecartOldPrice"></span></span>
                    <span style="font-size: 1.2rem; font-weight: bold; color: #15803d;">₹<span id="ecartNewPrice"></span></span>
                    <span style="background: #22c55e; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; font-weight: bold;">Save 15% (AgriMitra Exclusive)</span>
                </div>
                <button onclick="showToast('Added to Cart successfully!', 'success')" style="background: #166534; color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: bold; cursor: pointer; transition: 0.2s;"><i class="fa-solid fa-cart-shopping"></i> Purchase Now</button>
            </div>
        </div>
    </div>
'''

    if 'id="resultArea"' in html:
        idx = html.find('</div>\n\n{% endblock %}')
        if idx != -1:
            html = html[:idx] + ecart_html + html[idx:]
            with open('templates/crop.html', 'w', encoding='utf-8') as f:
                f.write(html)
            print('Injected e-cart into crop.html')
        else:
            print('Could not find injection point in crop.html')
    else:
        print('resultArea not found in crop.html')

def inject_fert():
    with open('templates/fertilizer.html', 'r', encoding='utf-8') as f:
        html = f.read()

    ecart_html = '''
    <!-- E-Commerce Section -->
    <div class="result-card" id="ecartSection" style="margin-top: 20px; background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border: 2px solid #22c55e;">
        <h4 style="color: #166534; font-weight: bold; margin-bottom: 15px;"><i class="fa-solid fa-store"></i> Buy Premium Fertilizer</h4>
        <div style="display: flex; gap: 15px; flex-wrap: wrap; align-items: center;">
            <div style="flex: 0 0 120px; height: 120px; border-radius: 10px; overflow: hidden; background: white; border: 1px solid #bbf7d0; display: flex; justify-content: center; align-items: center;">
                <img id="ecartImg" src="" alt="Fertilizer" style="max-width: 100%; max-height: 100%; object-fit: cover;">
            </div>
            <div style="flex: 1; min-width: 200px;">
                <h5 id="ecartTitle" style="margin-bottom: 5px; font-weight: 600; font-size: 1.1rem; color: #15803d;"></h5>
                <p id="ecartDesc" style="font-size: 0.9rem; color: #166534; margin-bottom: 10px;">High-grade nutrients for maximum crop growth.</p>
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                    <span style="text-decoration: line-through; color: #ef4444; font-size: 0.9rem;">₹<span id="ecartOldPrice"></span></span>
                    <span style="font-size: 1.2rem; font-weight: bold; color: #15803d;">₹<span id="ecartNewPrice"></span></span>
                    <span style="background: #22c55e; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; font-weight: bold;">Save 15% (AgriMitra Exclusive)</span>
                </div>
                <button onclick="showToast('Added to Cart successfully!', 'success')" style="background: #166534; color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: bold; cursor: pointer; transition: 0.2s;"><i class="fa-solid fa-cart-shopping"></i> Purchase Now</button>
            </div>
        </div>
    </div>
'''

    if 'id="resultArea"' in html:
        idx = html.find('</div>\n\n{% endblock %}')
        if idx != -1:
            html = html[:idx] + ecart_html + html[idx:]
            with open('templates/fertilizer.html', 'w', encoding='utf-8') as f:
                f.write(html)
            print('Injected e-cart into fertilizer.html')
        else:
            print('Could not find injection point in fertilizer.html')
    else:
        print('resultArea not found in fertilizer.html')

inject_crop()
inject_fert()
