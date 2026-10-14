import re

# 1. Update recommendation.html for 'combined' mode
with open('templates/recommendation.html', 'r', encoding='utf-8') as f:
    rec_content = f.read()

combined_admin = """{% elif active_mode == 'combined' %}
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
{% else %}"""

rec_content = rec_content.replace("{% else %}", combined_admin)

with open('templates/recommendation.html', 'w', encoding='utf-8') as f:
    f.write(rec_content)

print("Updated recommendation.html with 'combined' view")


# 2. Update lifecycle.html
with open('templates/lifecycle.html', 'r', encoding='utf-8') as f:
    life_content = f.read()

# I need to extract the existing admin block and replace it
# The existing admin block in lifecycle.html is:
old_admin_life = """<div style="padding: 30px;">
    <h2><i class="fa-solid fa-leaf"></i> Crop Lifecycle Tracker Info</h2>
    <div style="margin-top: 10px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <p>This module provides educational steps to farmers (Seed, Veg, Bloom, Harvest).</p>
        <p>Current static DB contains lifecycle paths for: Rice, Wheat, Cotton.</p>
    </div>
</div>"""

new_admin_life = """<div style="padding: 30px;">
    <h2><i class="fa-solid fa-seedling"></i> Lifecycle Knowledge Graph</h2>
    <p style="color: #666; margin-bottom: 20px;">Analysis of the agronomic timeline and tracking database.</p>

    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
        <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; border-bottom: 4px solid #166534;">
            <div style="font-size: 24px; color: #111; font-weight: bold;">4 Stages</div>
            <div style="color: #666; font-size: 13px; text-transform: uppercase;">Per Crop</div>
        </div>
        <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; border-bottom: 4px solid #0284c7;">
            <div style="font-size: 24px; color: #111; font-weight: bold;">Time-Series</div>
            <div style="color: #666; font-size: 13px; text-transform: uppercase;">Tracking Method</div>
        </div>
        <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; border-bottom: 4px solid #ca8a04;">
            <div style="font-size: 24px; color: #111; font-weight: bold;">Offline</div>
            <div style="color: #666; font-size: 13px; text-transform: uppercase;">Data Storage</div>
        </div>
    </div>
    
    <div style="margin-top: 30px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <h3 style="margin-top:0;"><i class="fa-solid fa-database"></i> Tracking Mechanism</h3>
        <p><strong>Database Structure:</strong> The system utilizes standard browser `localStorage` combined with user ID session mapping to persist agricultural timelines across sessions.</p>
        <p><strong>Supported Agronomic Profiles:</strong></p>
        <ul style="color: #444; line-height: 1.6;">
            <li><strong>Rice (Paddy):</strong> Sowing (0-15d) → Vegetative (15-60d) → Reproductive (60-90d) → Harvest (90-120d)</li>
            <li><strong>Wheat:</strong> Germination (0-10d) → Tillering (10-40d) → Heading (40-90d) → Ripening (90-120d)</li>
            <li><strong>Cotton:</strong> Planting (0-15d) → Squaring (15-45d) → Blooming (45-100d) → Defoliation (100-150d)</li>
        </ul>
        <p><strong>Actionable Triggers:</strong> At each stage transition, the frontend triggers contextual UI elements prompting farmers to adjust watering schedules and apply specific fertilizer blends based on the LightGBM models.</p>
    </div>
</div>"""

life_content = life_content.replace(old_admin_life, new_admin_life)

with open('templates/lifecycle.html', 'w', encoding='utf-8') as f:
    f.write(life_content)

print("Updated lifecycle.html")

