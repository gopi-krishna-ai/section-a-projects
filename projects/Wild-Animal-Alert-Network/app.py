import os
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from ultralytics import YOLO
import cv2
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RESULT_FOLDER'] = 'static/results'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

# Load a pretrained YOLO model trained on OpenImagesV7 (supports 600 classes including Tiger and Lion)
# Upgraded to yolov8x-oiv7.pt (Extra Large) for maximum possible accuracy
model = YOLO('yolov8x-oiv7.pt')

# Dictionary of animals with their properties (OpenImagesV7 class indices)
ANIMAL_INFO = {
    33: {"name": "Bear", "type": "Omnivorous", "wild": True, "avg_height": 1.5},
    49: {"name": "Bird", "type": "Omnivorous", "wild": False},
    96: {"name": "Cat", "type": "Carnivorous", "wild": False},
    99: {"name": "Cattle", "type": "Herbivorous", "wild": False},
    160: {"name": "Dog", "type": "Omnivorous", "wild": False},
    179: {"name": "Elephant", "type": "Herbivorous", "wild": True, "avg_height": 3.0},
    215: {"name": "Giraffe", "type": "Herbivorous", "wild": True, "avg_height": 5.0},
    255: {"name": "Horse", "type": "Herbivorous", "wild": False},
    313: {"name": "Lion", "type": "Carnivorous", "wild": True, "avg_height": 1.2},
    452: {"name": "Sheep", "type": "Herbivorous", "wild": False},
    534: {"name": "Tiger", "type": "Carnivorous", "wild": True, "avg_height": 1.1},
    599: {"name": "Zebra", "type": "Herbivorous", "wild": True, "avg_height": 1.5}
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/project')
def project():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        from flask import redirect, url_for
        return redirect(url_for('project'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        from flask import redirect, url_for
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/map')
def map_view():
    return render_template('map.html')

@app.route('/contact')
def contact_view():
    return render_template('contact.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        filename = secure_filename(file.filename)
        file_ext = os.path.splitext(filename)[1]
        unique_filename = str(uuid.uuid4()) + file_ext
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)

        # Run AI inference on the image
        results = model(filepath)
        
        detected_species = {}
        wild_detected = False
        total_animal_count = 0
        
        img = cv2.imread(filepath)
        
        # Process detection results
        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls = int(box.cls[0])
                if cls in ANIMAL_INFO:
                    total_animal_count += 1
                    animal = ANIMAL_INFO[cls]
                    
                    if animal['name'] not in detected_species:
                        detected_species[animal['name']] = animal.copy()
                        detected_species[animal['name']]['crops'] = []
                        
                    if animal["wild"]:
                        wild_detected = True
                        
                    # Crop the image using bounding box
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    h, w, _ = img.shape
                    x1, y1 = max(0, x1), max(0, y1)
                    x2, y2 = min(w, x2), min(h, y2)
                    
                    # Calculate estimated distance based on pixel height vs real height
                    if animal["wild"] and "avg_height" in animal:
                        bbox_h = y2 - y1
                        if bbox_h > 0:
                            focal_length = h * 0.8 # Rough focal length in pixels for standard webcams/phones
                            est_distance = round((animal['avg_height'] * focal_length) / bbox_h, 1)
                            
                            # Keep the closest distance if multiple are detected
                            current_est = detected_species[animal['name']].get('distance')
                            if current_est is None or est_distance < current_est:
                                detected_species[animal['name']]['distance'] = est_distance
                    
                    crop_img = img[y1:y2, x1:x2]
                    if crop_img.size > 0:
                        crop_filename = f"crop_{uuid.uuid4().hex[:8]}.jpg"
                        crop_path = os.path.join(app.config['RESULT_FOLDER'], crop_filename)
                        cv2.imwrite(crop_path, crop_img)
                        detected_species[animal['name']]['crops'].append(f'/static/results/{crop_filename}')
            
            # Save the analyzed image with bounding boxes drawn
            res_img_path = os.path.join(app.config['RESULT_FOLDER'], unique_filename)
            r.save(filename=res_img_path)
            
        animals_list = list(detected_species.values())
        
        if wild_detected:
            status = 'danger'
            names = ", ".join([a['name'] for a in animals_list if a['wild']])
            summary = f"Wild animal(s) detected: {names}. Alarm triggered! Proceed with caution."
        elif animals_list:
            status = 'safe'
            names = ", ".join([a['name'] for a in animals_list])
            summary = f"Detected safe animal(s): {names}. Area is secure."
        else:
            status = 'clear'
            summary = "No animals detected. Area is clear."
            
        return jsonify({
            'success': True,
            'wild_detected': wild_detected,
            'status': status,
            'animals': animals_list,
            'total_count': total_animal_count,
            'image_url': f'/static/results/{unique_filename}',
            'summary': summary
        })

if __name__ == '__main__':
    print("Starting Wild Animal Alert System Server on http://127.0.0.1:8080")
    app.run(debug=True, use_reloader=False, port=8080)
