import os
import re

base_dir = r'C:\Users\krish\OneDrive\Desktop\section a\TrafficControlSystem'
html_path = os.path.join(base_dir, 'templates', 'dashboard.html')

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pre-fill the YouTube URL in the Input Feed
old_input = '''<input type="text" id="cameraUrl" placeholder="e.g., https://camera-stream.local/cam1" style="width:100%; padding:10px; border-radius:8px; border:1px solid var(--border); background:rgba(255,255,255,0.05); color:white;">'''
new_input = '''<input type="text" id="cameraUrl" value="https://www.youtube.com/watch?v=wqctLW0Hb_0" placeholder="e.g., https://camera-stream.local/cam1" style="width:100%; padding:10px; border-radius:8px; border:1px solid var(--border); background:rgba(255,255,255,0.05); color:white;">'''
content = content.replace(old_input, new_input)

# Add a video container to the AI Analytics panel
old_panel = '''                <img id="processedImage" src="" alt="Awaiting Feed" style="width:100%; border-radius:12px; border:2px solid var(--border); display:none;">'''
new_panel = '''                <div id="videoContainer" style="width:100%; aspect-ratio: 16/9; border-radius:12px; border:2px solid var(--border); overflow:hidden; display:none; margin-bottom:15px;">
                    <iframe id="youtubePlayer" width="100%" height="100%" src="" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
                </div>
                <img id="processedImage" src="" alt="Awaiting Feed" style="width:100%; border-radius:12px; border:2px solid var(--border); display:none; margin-bottom:15px;">'''
content = content.replace(old_panel, new_panel)

# Update the Javascript to handle YouTube URLs
old_js = '''                document.getElementById('processedImage').src = data.image;
                document.getElementById('processedImage').style.display = 'block';
                if (document.getElementById('mlOptimalTime') && data.ml_optimal_time) {'''

new_js = '''                let sourceUrl = document.getElementById('cameraUrl').value;
                if (sourceUrl.includes("youtube.com/watch?v=")) {
                    let videoId = sourceUrl.split("v=")[1].substring(0, 11);
                    document.getElementById('youtubePlayer').src = "https://www.youtube.com/embed/" + videoId + "?autoplay=1&mute=1";
                    document.getElementById('videoContainer').style.display = 'block';
                    document.getElementById('processedImage').style.display = 'none';
                } else {
                    document.getElementById('processedImage').src = data.image;
                    document.getElementById('processedImage').style.display = 'block';
                    document.getElementById('videoContainer').style.display = 'none';
                }
                
                if (document.getElementById('mlOptimalTime') && data.ml_optimal_time) {'''
content = content.replace(old_js, new_js)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
