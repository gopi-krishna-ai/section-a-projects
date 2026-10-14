import os

base_dir = r'C:\Users\krish\OneDrive\Desktop\section a\TrafficControlSystem'
app_path = os.path.join(base_dir, 'app.py')

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the unsplash IDs with guaranteed traffic/road images
old_frames = '''    # Multiple mock frames to simulate video extraction
    mock_frames = [
        "https://images.unsplash.com/photo-1542385151-efd9000785a0?w=400&q=80",
        "https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=400&q=80",
        "https://images.unsplash.com/photo-1449844908441-8829872d2607?w=400&q=80"
    ]'''

new_frames = '''    # Multiple mock frames to simulate video extraction (Actual traffic images)
    mock_frames = [
        "https://images.unsplash.com/photo-1449844908441-8829872d2607?w=800&q=80", # Traffic
        "https://images.unsplash.com/photo-1520106981881-a67b5eb604f3?w=800&q=80", # Traffic
        "https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=800&q=80"  # Traffic
    ]'''

content = content.replace(old_frames, new_frames)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)
