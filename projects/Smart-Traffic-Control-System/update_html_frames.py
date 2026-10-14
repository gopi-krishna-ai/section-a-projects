import os

base_dir = r'C:\Users\krish\OneDrive\Desktop\section a\TrafficControlSystem'
html_path = os.path.join(base_dir, 'templates', 'dashboard.html')

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add UI for Summary and Gallery
old_ui = '''<div class="panel">
                <h3>Live Camera Frame</h3>
                <img id="processedImage" src="" alt="Awaiting Feed" style="width:100%; border-radius:12px; border:2px solid var(--border);">
            </div>'''

new_ui = '''<div class="panel">
                <h3>Analysis Summary</h3>
                <div id="analysisSummary" style="background:#1e293b; padding:15px; border-radius:10px; color:#cbd5e1; font-size:15px; line-height:1.6; border:1px solid var(--border); margin-bottom: 20px;">
                    Awaiting feed analysis...
                </div>
                <h3>Key Extracted Frames</h3>
                <div id="framesGallery" style="display:flex; gap:10px; overflow-x:auto; padding-bottom:10px; margin-bottom:15px;">
                    <!-- Frames will be injected here -->
                </div>
                <img id="processedImage" src="" alt="Awaiting Feed" style="width:100%; border-radius:12px; border:2px solid var(--border); display:none;">
            </div>'''

content = content.replace(old_ui, new_ui)

# Make sure we send the URL in the JS fetch
old_js_fetch = '''            fetch('/api/analyze_traffic', { method: 'POST' })
                .then(r => r.json())'''

new_js_fetch = '''            let formData = new FormData();
            formData.append('url', document.getElementById('cameraUrl').value);
            fetch('/api/analyze_traffic', { method: 'POST', body: formData })
                .then(r => r.json())'''

content = content.replace(old_js_fetch, new_js_fetch)

# Update the JS to populate the new UI
old_js_populate = '''                document.getElementById('processedImage').src = data.image;
                if (document.getElementById('mlOptimalTime') && data.ml_optimal_time) {
                    document.getElementById('mlOptimalTime').innerText = data.ml_optimal_time;
                }'''

new_js_populate = '''                document.getElementById('processedImage').src = data.image;
                document.getElementById('processedImage').style.display = 'block';
                if (document.getElementById('mlOptimalTime') && data.ml_optimal_time) {
                    document.getElementById('mlOptimalTime').innerText = data.ml_optimal_time;
                }
                if (data.summary) {
                    document.getElementById('analysisSummary').innerHTML = data.summary;
                }
                if (data.frames) {
                    let gallery = document.getElementById('framesGallery');
                    gallery.innerHTML = '';
                    data.frames.forEach(frameSrc => {
                        let img = document.createElement('img');
                        img.src = frameSrc;
                        img.style.height = '120px';
                        img.style.borderRadius = '8px';
                        img.style.border = '1px solid #334155';
                        gallery.appendChild(img);
                    });
                }'''

content = content.replace(old_js_populate, new_js_populate)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
