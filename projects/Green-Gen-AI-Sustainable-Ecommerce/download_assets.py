import os
import urllib.request

ASSETS = {
    'static/js/three.min.js': 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js',
    'static/js/OrbitControls.js': 'https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js',
    'static/css/all.min.css': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
    'static/webfonts/fa-solid-900.woff2': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/webfonts/fa-solid-900.woff2',
    'static/webfonts/fa-solid-900.ttf': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/webfonts/fa-solid-900.ttf',
}

def download_assets():
    for path, url in ASSETS.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        print(f"Downloading {url} to {path}...")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                with open(path, 'wb') as f:
                    f.write(response.read())
            print(f"Success: {path}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")

if __name__ == '__main__':
    download_assets()
