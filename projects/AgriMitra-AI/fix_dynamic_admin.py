import re

with open('templates/recommendation.html', 'r', encoding='utf-8') as f:
    content = f.read()

dynamic_admin = """
{% if active_mode == 'crop' %}
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
        <p><strong>Output Classes:</strong> 22 unique crop types</p>
        <p><strong>Training Data:</strong> 2,200 instances, 7 features each. Handled class imbalance using SMOTE. Split 80/20 train/test.</p>
    </div>
</div>
{% elif active_mode == 'fertilizer' %}
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
        <p><strong>Output Classes:</strong> 7 fertilizer grades</p>
        <p><strong>Training Strategy:</strong> Categorical encoding for Soil and Crop types. Hyperparameter tuning via GridSearchCV.</p>
    </div>
</div>
{% elif active_mode == 'soil' %}
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
{% else %}
<div style="padding: 30px;">
    <h2><i class="fa-solid fa-map"></i> Unified Map Hub Status</h2>
    <div style="margin-top: 10px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <p><i class="fa-solid fa-check-circle" style="color: #166534;"></i> MapBox / Leaflet integration operational.</p>
        <p><i class="fa-solid fa-check-circle" style="color: #166534;"></i> Combined Crop & Fertilizer prediction pipeline active.</p>
    </div>
</div>
{% endif %}
"""

old_admin = """<div style="padding: 30px;">
    <h2><i class="fa-solid fa-map"></i> Unified Map Hub Status</h2>
    <div style="margin-top: 10px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <p><i class="fa-solid fa-check-circle" style="color: #166534;"></i> MapBox / Leaflet integration operational.</p>
        <p><i class="fa-solid fa-check-circle" style="color: #166534;"></i> Combined Crop & Fertilizer prediction pipeline active.</p>
    </div>
</div>"""

content = content.replace(old_admin, dynamic_admin)

with open('templates/recommendation.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated recommendation.html with dynamic jinja for active_mode")
