import os

base_dir = r'C:\Users\krish\OneDrive\Desktop\section a\01_GuardPath_AI_Updated\B-1-GuardPath AI'
readme_path = os.path.join(base_dir, 'README.md')

with open(readme_path, 'r', encoding='utf-8') as f:
    readme = f.read()

new_setup_section = """## Setup & Run

`ash
cd "B-1-GuardPath AI"
python -m venv venv 
# On Windows
.\\venv\\Scripts\\activate
# On Mac/Linux
# source venv/bin/activate

pip install -r requirements.txt

# 1. (Optional) Rebuild city_areas.csv + city_graph.py
python data/process_kaggle_dataset.py

# 2. Generate the simulated ML training dataset
python data/generate_dataset.py

# 3. Train the Random Forest model
python model/train_model.py

# 4. Run the web app
python app.py
`

Then open **http://127.0.0.1:5000/** in a browser. 
You will be greeted by the new **Landing Page**. Click **Login to Start**.

### Test Credentials
* **Admin Role:** dmin / dmin
* **Passenger 1:** passenger1 / pass1
* **Passenger 2:** passenger2 / pass2

Once logged in, you can access the map, set sources/destinations, and access your **Ride History** (showing the last 10 rides and the road suggestions used).

## Reference Datasets (Kaggle)"""

import re
readme = re.sub(r'## Setup & Run.*?(?=## Reference Datasets \(Kaggle\))', lambda m: new_setup_section + "\n\n", readme, flags=re.DOTALL)

with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(readme)
