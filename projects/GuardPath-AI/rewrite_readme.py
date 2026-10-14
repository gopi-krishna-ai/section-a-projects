import os

base_dir = r'C:\Users\krish\OneDrive\Desktop\section a\01_GuardPath_AI_Updated\B-1-GuardPath AI'
readme_path = os.path.join(base_dir, 'README.md')

new_content = '''# GuardPath AI 🛡️
**AI-Powered Personal Safety & Smart Route Planner**

GuardPath AI is an intelligent navigation and safety platform that prioritizes user security over mere distance. By leveraging Machine Learning (Random Forest algorithms) and real-world telemetry data, it calculates the safest possible routes for pedestrians and drivers.

---

## ✨ Features (Latest Additions)

* **🧠 AI Safety Engine:** Predicts route safety (Safe, Moderate, Unsafe) using Machine Learning based on road conditions, traffic density, crime rates, and lighting.
* **🗺️ Interactive Live Map:** Powered by Leaflet & OpenStreetMap, displaying live-style map markers, actual road geometry (OSRM), and traffic visualizations.
* **🚧 Community Hazard Reporting:** Users can upload images and report roadblocks or hazards directly onto the community map.
* **🚨 SOS Emergency Dispatch:** A floating SOS button that triggers instant emergency alerts (via email) to trusted contacts, complete with live GPS coordinates.
* **⏱️ Safety Check Monitor:** Simulates trip monitoring. If a user stops unexpectedly, the system triggers a 15-second "Are you safe?" countdown before auto-dispatching SOS.
* **👤 User Registration & Sessions:** Full authentication system (stored in data/users.json). Users can register, login, and view their personalized ride history.
* **👑 Admin Dashboard:** Dedicated dashboard for administrators to monitor active SOS alerts, community-reported hazards (with image evidence), and global trip histories.
* **💎 Premium Glassmorphism UI:** A stunning, modern, responsive design with frosted glass panels, animated gradients, and Tailwind-inspired aesthetics.

---

## 🛠️ Setup & Run Instructions

**1. Create & Activate Virtual Environment:**
`ash
cd "B-1-GuardPath AI"
python -m venv venv 

# On Windows:
.\\venv\\Scripts\\activate
# On Mac/Linux:
# source venv/bin/activate
`

**2. Install Dependencies:**
`ash
pip install -r requirements.txt
`

**3. Run the Application:**
`ash
python app.py
`
Then open **http://127.0.0.1:5000/** in a web browser.

---

## 🚀 Demo Guide & Test Credentials

### Logging In
You can register a new account on the Login page, or use the pre-configured test credentials:
* **Admin Dashboard:** dmin / dmin
* **Passenger 1:** passenger1 / pass1
* **Passenger 2:** passenger2 / pass2

### Testing the Features
* **Route Planning:** Login as a passenger, select a Source and Destination on the map, and click "Find Safest Route" to see the ML model in action.
* **Hazard Reporting:** Click the amber 🚧 button on the bottom left. Fill out the description to instantly drop a community warning on the map.
* **Safety Monitor Countdown:** Click "Start Trip" on any suggested route. A 15-second safety countdown will automatically pop up to ensure passenger safety.
* **Admin View:** Login as dmin to see all logged SOS alerts, passenger histories, and uploaded hazard reports.

---

## 📧 Enabling Real SOS Email Dispatch (Optional)

By default, the SOS Emergency feature runs in **Simulation Mode** (it prints the dispatch receipt to the console without sending a real email). If you want the prototype to send **real emails** during your demo, follow these steps:

1. Open pp.py in your code editor.
2. Locate the **Email Configuration** section at the very top (around Line 11):
   `python
   SENDER_EMAIL = 'your_email@gmail.com'
   SENDER_PASSWORD = 'your_app_password'
   `
3. Replace 'your_email@gmail.com' with your actual Gmail address.
4. Replace 'your_app_password' with a **16-letter Google App Password**. 
   *(Note: For security reasons, Google does not allow your normal login password here. You must go to your Google Account Settings -> Security -> 2-Step Verification -> **App Passwords** to generate one for this script).*

Once configured and saved, the application will successfully route SOS alerts to any email address provided in the SOS modal!

---

## 📊 Real-World Data Source & Methodology
Safety metrics (	raffic_level, oad_condition, crime_rate, lighting_condition) are derived from a dataset of **207,617 real, GPS-tagged alerts** logged by a Collision Avoidance System fitted to vehicles driving through Bangalore (data/kaggle_reference/bangalore_cas/bangalore-cas-alerts.csv). The Machine Learning model (	rain_model.py) is trained on a simulated dataset generated from these real-world statistical baselines.
'''

with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully rewrote README.md")
