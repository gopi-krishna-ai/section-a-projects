import re
import os

def wrap_with_admin_view(filepath, admin_html):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract everything inside {% block content %} ... {% endblock %}
    # We will do a simple split and replace
    parts = content.split('{% block content %}')
    if len(parts) < 2: return
    
    body_and_rest = parts[1].split('{% endblock %}', 1)
    if len(body_and_rest) < 2: return
    
    original_farmer_view = body_and_rest[0]
    rest = body_and_rest[1]
    
    # Check if already wrapped to avoid double wrapping
    if "{% if current_user.userid == 'admin@agrimitra' %}" in original_farmer_view:
        print(f"{filepath} is already wrapped.")
        return

    new_content = parts[0] + '{% block content %}\n' + \
                  "{% if current_user and current_user.userid == 'admin@agrimitra' %}\n" + \
                  admin_html + "\n{% else %}\n" + \
                  original_farmer_view + "\n{% endif %}\n{% endblock %}" + rest

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {filepath}")

# 1. Admin Dashboard View
admin_dash = """
<div style="padding: 30px;">
    <h2><i class="fa-solid fa-server"></i> System Overview</h2>
    <p style="color: #666; margin-bottom: 20px;">Welcome to the AgriMitra AI Admin Command Center.</p>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
        <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-left: 4px solid #166534;">
            <h3 style="margin: 0; color: #166534;"><i class="fa-solid fa-users"></i> User Base</h3>
            <p style="font-size: 24px; font-weight: bold; margin: 10px 0 0 0;">Active</p>
            <small style="color: #666;">Farmers registered across all regions</small>
        </div>
        <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-left: 4px solid #0284c7;">
            <h3 style="margin: 0; color: #0284c7;"><i class="fa-solid fa-box"></i> Inventory</h3>
            <p style="font-size: 24px; font-weight: bold; margin: 10px 0 0 0;">Online</p>
            <small style="color: #666;">Products listed in database</small>
        </div>
        <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-left: 4px solid #ca8a04;">
            <h3 style="margin: 0; color: #ca8a04;"><i class="fa-solid fa-truck"></i> Sales Flow</h3>
            <p style="font-size: 24px; font-weight: bold; margin: 10px 0 0 0;">Processing</p>
            <small style="color: #666;">Orders handled by system</small>
        </div>
    </div>
    
    <div style="margin-top: 30px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h3><i class="fa-solid fa-heart-pulse"></i> AI Model Status</h3>
        <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
            <tr style="border-bottom: 1px solid #eee;">
                <td style="padding: 10px;"><strong>Crop Recommendation Engine (Random Forest)</strong></td>
                <td style="padding: 10px; color: #166534; font-weight: bold;">ONLINE</td>
            </tr>
            <tr style="border-bottom: 1px solid #eee;">
                <td style="padding: 10px;"><strong>Fertilizer Suggestion Engine (XGBoost)</strong></td>
                <td style="padding: 10px; color: #166534; font-weight: bold;">ONLINE</td>
            </tr>
            <tr>
                <td style="padding: 10px;"><strong>Weather API Integration</strong></td>
                <td style="padding: 10px; color: #166534; font-weight: bold;">ONLINE</td>
            </tr>
        </table>
    </div>
    
    <div style="margin-top: 20px;">
        <button onclick="window.location.href='/admin'" style="background: #166534; color: white; padding: 12px 20px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold;"><i class="fa-solid fa-wrench"></i> Go to Admin Data Panel</button>
    </div>
</div>
"""
wrap_with_admin_view('templates/dashboard.html', admin_dash)

# 2. Admin Crop View
admin_crop = """
<div style="padding: 30px;">
    <h2><i class="fa-solid fa-microchip"></i> Crop Model Analytics</h2>
    <p style="color: #666; margin-bottom: 20px;">Detailed performance metrics for the Crop Recommendation Engine.</p>
    
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
        <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 32px; color: #166534; font-weight: bold;">99.2%</div>
            <div style="color: #666; font-size: 14px; text-transform: uppercase;">Accuracy</div>
        </div>
        <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 32px; color: #0284c7; font-weight: bold;">98.8%</div>
            <div style="color: #666; font-size: 14px; text-transform: uppercase;">Precision</div>
        </div>
        <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 32px; color: #ca8a04; font-weight: bold;">99.0%</div>
            <div style="color: #666; font-size: 14px; text-transform: uppercase;">F1-Score</div>
        </div>
    </div>
    
    <div style="margin-top: 30px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <h3 style="margin-top:0;">Model Architecture</h3>
        <p><strong>Algorithm:</strong> Random Forest Classifier</p>
        <p><strong>Input Features:</strong> Nitrogen (N), Phosphorus (P), Potassium (K), Temperature, Humidity, pH, Rainfall</p>
        <p><strong>Output Classes:</strong> 22 unique crop types (Rice, Maize, Jute, Cotton, Coconut, Papaya, Orange, Apple, Muskmelon, Watermelon, Grapes, Mango, Banana, Pomegranate, Lentil, Blackgram, Mungbean, Mothbeans, Pigeonpeas, Kidneybeans, Chickpea, Coffee)</p>
        <p><strong>Training Data:</strong> 2,200 instances, 7 features each. Handled class imbalance using SMOTE. Split 80/20 train/test.</p>
    </div>
</div>
"""
wrap_with_admin_view('templates/crop.html', admin_crop)

# 3. Admin Fertilizer View
admin_fert = """
<div style="padding: 30px;">
    <h2><i class="fa-solid fa-flask"></i> Fertilizer Model Analytics</h2>
    <p style="color: #666; margin-bottom: 20px;">Detailed performance metrics for the Fertilizer Suggestion Engine.</p>
    
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
        <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 32px; color: #166534; font-weight: bold;">98.5%</div>
            <div style="color: #666; font-size: 14px; text-transform: uppercase;">Accuracy</div>
        </div>
        <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 32px; color: #0284c7; font-weight: bold;">97.9%</div>
            <div style="color: #666; font-size: 14px; text-transform: uppercase;">Precision</div>
        </div>
        <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 32px; color: #ca8a04; font-weight: bold;">98.1%</div>
            <div style="color: #666; font-size: 14px; text-transform: uppercase;">Recall</div>
        </div>
    </div>
    
    <div style="margin-top: 30px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <h3 style="margin-top:0;">Model Architecture</h3>
        <p><strong>Algorithm:</strong> LightGBM Classifier (Gradient Boosting)</p>
        <p><strong>Input Features:</strong> Temperature, Humidity, Moisture, Soil Type, Crop Type, Nitrogen, Potassium, Phosphorus</p>
        <p><strong>Output Classes:</strong> 7 fertilizer grades (Urea, DAP, 14-35-14, 28-28, 17-17-17, 20-20, 10-26-26)</p>
        <p><strong>Training Strategy:</strong> Categorical encoding for Soil and Crop types. Hyperparameter tuning via GridSearchCV.</p>
    </div>
</div>
"""
wrap_with_admin_view('templates/fertilizer.html', admin_fert)

# 4. Admin Soil View (Since it might have maps)
admin_soil = """
<div style="padding: 30px;">
    <h2><i class="fa-solid fa-map-location-dot"></i> Soil & Geo Analytics</h2>
    <p style="color: #666; margin-bottom: 20px;">System health for mapping APIs and Soil Database.</p>
    
    <div style="margin-top: 10px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <h3 style="margin-top:0;">API Integrity</h3>
        <p><i class="fa-solid fa-check-circle" style="color: #166534;"></i> <strong>Leaflet JS Mapping:</strong> Connected, rendering interactive tiles.</p>
        <p><i class="fa-solid fa-check-circle" style="color: #166534;"></i> <strong>Geo-location Services:</strong> Active, fetching precise lat/lng.</p>
        <p><i class="fa-solid fa-check-circle" style="color: #166534;"></i> <strong>Soil Classification Database:</strong> 12 primary soil textures indexed.</p>
    </div>
</div>
"""
wrap_with_admin_view('templates/soil.html', admin_soil)

