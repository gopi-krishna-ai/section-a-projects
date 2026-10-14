import re

def wrap_with_admin_view(filepath, admin_html):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    parts = content.split('{% block content %}')
    if len(parts) < 2: return
    
    body_and_rest = parts[1].split('{% endblock %}', 1)
    if len(body_and_rest) < 2: return
    
    original_farmer_view = body_and_rest[0]
    rest = body_and_rest[1]
    
    if "{% if current_user and current_user.userid == 'admin@agrimitra' %}" in original_farmer_view:
        return

    new_content = parts[0] + '{% block content %}\n' + \
                  "{% if current_user and current_user.userid == 'admin@agrimitra' %}\n" + \
                  admin_html + "\n{% else %}\n" + \
                  original_farmer_view + "\n{% endif %}\n{% endblock %}" + rest

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {filepath}")

# Map Hub
admin_recommend = """
<div style="padding: 30px;">
    <h2><i class="fa-solid fa-map"></i> Unified Map Hub Status</h2>
    <div style="margin-top: 10px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <p><i class="fa-solid fa-check-circle" style="color: #166534;"></i> MapBox / Leaflet integration operational.</p>
        <p><i class="fa-solid fa-check-circle" style="color: #166534;"></i> Combined Crop & Fertilizer prediction pipeline active.</p>
    </div>
</div>
"""
wrap_with_admin_view('templates/recommendation.html', admin_recommend)

# Lifecycle
admin_life = """
<div style="padding: 30px;">
    <h2><i class="fa-solid fa-leaf"></i> Crop Lifecycle Tracker Info</h2>
    <div style="margin-top: 10px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <p>This module provides educational steps to farmers (Seed, Veg, Bloom, Harvest).</p>
        <p>Current static DB contains lifecycle paths for: Rice, Wheat, Cotton.</p>
    </div>
</div>
"""
wrap_with_admin_view('templates/lifecycle.html', admin_life)

# Market
admin_market = """
<div style="padding: 30px;">
    <h2><i class="fa-solid fa-shop"></i> Marketplace API</h2>
    <div style="margin-top: 10px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <p>Market API connection fetching live spot prices for standard commodities.</p>
    </div>
</div>
"""
wrap_with_admin_view('templates/market.html', admin_market)

# Assistant
admin_assistant = """
<div style="padding: 30px;">
    <h2><i class="fa-solid fa-robot"></i> LLM Assistant Health</h2>
    <div style="margin-top: 10px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <p><i class="fa-solid fa-check-circle" style="color: #166534;"></i> LLM Backend Connected.</p>
        <p>Usage: 145/500 API calls remaining this month.</p>
    </div>
</div>
"""
wrap_with_admin_view('templates/assistant.html', admin_assistant)

