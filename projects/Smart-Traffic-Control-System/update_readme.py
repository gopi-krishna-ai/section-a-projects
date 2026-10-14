import os

base_dir = r'C:\Users\krish\OneDrive\Desktop\section a\TrafficControlSystem'
readme_path = os.path.join(base_dir, 'README.md')

new_content = '''# Intelligent Traffic Control System 🚦

Our application uses Computer Vision and Machine Learning to automatically monitor vehicle congestion and dynamically adjust traffic signals. It features a real-time smart dashboard for city authorities to manually adjust safety thresholds, monitor city-wide congestion maps, and track transit complaints.

---

## ✨ Key Features

1. **Live Feed Input**: Process live surveillance camera feeds or uploaded video files.
2. **AI Computer Vision Dashboard**: Visualizes bounding boxes and provides live vehicle counting (simulating YOLOv8 object detection).
3. **🧠 Machine Learning Optimization (NEW)**: Integrates a trained **Random Forest Regressor** that analyzes live vehicle counts, the time of day (rush hour vs normal), and weather conditions to dynamically predict the **Optimal Green Light Time** in seconds.
4. **Adaptive Signal Control**: Dynamically changes a virtual traffic light to RED if the vehicle count exceeds the set threshold to prevent gridlock.
5. **Congestion Map**: An interactive map of India (Leaflet.js) to monitor high-traffic zones and police control rooms.
6. **Transit Complaint System**: A dedicated route-reporting tool to flag signal failures or congestion between specific checkpoints.
7. **Dynamic Settings**: Administrators can instantly slide and adjust the AI congestion threshold in real time without restarting the system.

---

## 📂 Project Structure

`	ext
TrafficControlSystem/
├── app.py                  # Main Flask API and Backend Logic
├── requirements.txt        # Python dependencies
├── README.md               # Documentation
├── ml/                     # Machine Learning Pipeline
│   ├── train_model.py      # Script to generate dataset & train the ML model
│   ├── traffic_data.csv    # Synthetic training dataset
│   └── models/
│       └── green_time_model.pkl # Trained Random Forest model
├── static/
│   └── css/
│       └── style.css       # Premium Dark-Mode Glassmorphism UI
└── templates/
    ├── landing.html        # Welcome / Explanation Screen
    ├── login.html          # Authentication Screen
    └── dashboard.html      # 6-Tab Single Page Application (SPA)
`

---

## ⚙️ Installation & Setup

1. **Navigate to the Project**:
   `ash
   cd TrafficControlSystem
   `
2. **Set up a Virtual Environment**:
   `ash
   python -m venv venv
   # On Windows:
   .\\venv\\Scripts\\activate
   # On Mac/Linux:
   # source venv/bin/activate
   `
3. **Install Dependencies**:
   `ash
   pip install -r requirements.txt
   `
4. **(Optional) Retrain the Machine Learning Model**:
   `ash
   python ml/train_model.py
   `
5. **Run the Application**:
   `ash
   python app.py
   `
6. **Access the App**:
   Open **http://127.0.0.1:5001** in your browser.

---

## 🚀 How to Use the Application

Once you have opened the app in your web browser, follow these steps to test the full flow:

1. **Login**: Click "Launch System Dashboard" on the landing page, then enter any mock credentials (e.g., dmin@traffic.gov) to log in.
2. **Input Traffic Feed**: On the **Input Feed** tab, either upload a sample video file OR paste a live camera URL. Click **Initiate AI Scanning**.
3. **View AI Results**: The system will automatically switch to the **AI Analytics** tab. Here you will see:
   - The processed camera frame.
   - The real-time vehicle count.
   - The **Machine Learning Predicted Optimal Green Light Time**.
4. **Check Traffic Signal**: Click the **Live Signal** tab. You will see a glowing traffic light dynamically set to RED or GREEN based on the number of detected vehicles.
5. **Adjust the Rules**: Go to the **Settings** tab. Use the slider to change the maximum allowed vehicle threshold (e.g., from 10 to 20). Go back to step 2 and scan again to see how the signal adapts to your new rules!
6. **Monitor the Map**: Open the **Congestion Map** tab, type in a city (like "Mumbai"), and click "Plot Traffic Data" to see mock high-congestion zones plotted around the city.

---

## 🎥 Demo Video Datasets for Testing

If you want to test the application with realistic data during a presentation, you can download sample traffic surveillance videos from these open-source datasets:
*   **Kaggle Traffic Video Dataset**: [Vehicles on the road](https://www.kaggle.com/datasets/aryashah2k/vehicles-on-the-road-traffic-video)
*   **YouTube Sample Feed**: You can paste a link like https://www.youtube.com/watch?v=wqctLW0Hb_0 (Live Traffic Cam) into the URL Input.

*(Note: For this web prototype, the backend simulates the heavy Computer Vision processing so the dashboard remains incredibly fast and responsive during presentations. However, the Machine Learning timing prediction runs on a genuine, trained Scikit-Learn model!)*
'''

with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated README.md for TrafficControlSystem")
