import os

base_dir = r'C:\Users\krish\OneDrive\Desktop\section a\01_GuardPath_AI_Updated\B-1-GuardPath AI'
app_path = os.path.join(base_dir, 'app.py')

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace empty HAZARDS and SOS_ALERTS with Demo Data
old_lists = '''# New Data stores for Community Hazards and SOS
HAZARDS = []
SOS_ALERTS = []'''

new_lists = '''# New Data stores for Community Hazards and SOS (PRE-LOADED DEMO DATA)
HAZARDS = [
    {
        'id': 'demo-haz-1',
        'user': 'passenger2',
        'name': 'Bob',
        'description': 'Severe waterlogging under the bridge, traffic at standstill.',
        'lat': 12.9172,
        'lng': 77.6228,
        'image': None,
        'timestamp': (datetime.now() - timedelta(minutes=45)).strftime('%Y-%m-%d %H:%M:%S')
    },
    {
        'id': 'demo-haz-2',
        'user': 'passenger1',
        'name': 'Alice',
        'description': 'Fallen tree blocking the left lane on main road.',
        'lat': 12.9716,
        'lng': 77.5946,
        'image': None,
        'timestamp': (datetime.now() - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
    }
]

SOS_ALERTS = [
    {
        'id': 'demo-sos-1',
        'user': 'passenger2',
        'name': 'Bob',
        'lat': 12.9352,
        'lng': 77.6245,
        'email': 'family.emergency@example.com',
        'message': 'My cab took a wrong turn into a dark alley and driver is acting suspicious.',
        'timestamp': (datetime.now() - timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')
    }
]'''

if old_lists in content:
    content = content.replace(old_lists, new_lists)
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Demo data injected successfully.")
else:
    print("Could not find the exact string to replace. It might already be injected.")
