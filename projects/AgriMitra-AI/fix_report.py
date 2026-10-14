import re

with open('templates/report.html', 'r', encoding='utf-8') as f:
    content = f.read()

admin_report = """
<div style="padding: 30px;">
    <h2><i class="fa-solid fa-network-wired"></i> Complete Recommendation Pipeline</h2>
    <p style="color: #666; margin-bottom: 20px;">Architecture overview of the Unified Farm Analysis Engine.</p>
    
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
        <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; border-bottom: 4px solid #166534;">
            <div style="font-size: 24px; color: #111; font-weight: bold;">Sequential</div>
            <div style="color: #666; font-size: 13px; text-transform: uppercase;">Inference Mode</div>
        </div>
        <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; border-bottom: 4px solid #0284c7;">
            <div style="font-size: 24px; color: #111; font-weight: bold;">1.2s</div>
            <div style="color: #666; font-size: 13px; text-transform: uppercase;">Avg Pipeline Latency</div>
        </div>
        <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; border-bottom: 4px solid #ca8a04;">
            <div style="font-size: 24px; color: #111; font-weight: bold;">REST API</div>
            <div style="color: #666; font-size: 13px; text-transform: uppercase;">Protocol</div>
        </div>
    </div>
    
    <div style="margin-top: 30px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <h3 style="margin-top:0;"><i class="fa-solid fa-diagram-project"></i> Pipeline Execution Flow</h3>
        
        <div style="display: flex; flex-direction: column; gap: 15px; margin-top: 20px;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="background: #e2e8f0; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 50%; font-weight: bold; color: #475569;">1</div>
                <div>
                    <strong style="font-size: 15px;">Geo-Spatial Intake</strong>
                    <p style="margin: 3px 0 0 0; font-size: 13px; color: #666;">Browser geolocation captures Lat/Lng and fetches reverse-geocoded farm address.</p>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="background: #e2e8f0; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 50%; font-weight: bold; color: #475569;">2</div>
                <div>
                    <strong style="font-size: 15px;">Climate API Aggregation</strong>
                    <p style="margin: 3px 0 0 0; font-size: 13px; color: #666;">OpenWeather API resolves live temperature, humidity, and atmospheric pressure.</p>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="background: #e2e8f0; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 50%; font-weight: bold; color: #475569;">3</div>
                <div>
                    <strong style="font-size: 15px;">Crop Inference (Random Forest)</strong>
                    <p style="margin: 3px 0 0 0; font-size: 13px; color: #666;">Yields Top 3 crops based on soil inputs and fetched climate data.</p>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="background: #e2e8f0; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 50%; font-weight: bold; color: #475569;">4</div>
                <div>
                    <strong style="font-size: 15px;">Fertilizer Inference (LightGBM)</strong>
                    <p style="margin: 3px 0 0 0; font-size: 13px; color: #666;">Takes the #1 recommended crop and calculates exact NPK deficiencies to recommend fertilizers.</p>
                </div>
            </div>
        </div>
    </div>
</div>
"""

# Same approach as before
parts = content.split('{% block content %}')
if len(parts) >= 2:
    body_and_rest = parts[1].split('{% endblock %}', 1)
    if len(body_and_rest) >= 2:
        original_farmer_view = body_and_rest[0]
        rest = body_and_rest[1]
        
        if "{% if current_user and current_user.userid == 'admin@agrimitra' %}" not in original_farmer_view:
            new_content = parts[0] + '{% block content %}\n' + \
                          "{% if current_user and current_user.userid == 'admin@agrimitra' %}\n" + \
                          admin_report + "\n{% else %}\n" + \
                          original_farmer_view + "\n{% endif %}\n{% endblock %}" + rest
                          
            with open('templates/report.html', 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Fixed report.html")
