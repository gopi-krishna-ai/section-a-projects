# 🧠 StudyAI: Advanced Smart Study Planner

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![React](https://img.shields.io/badge/Frontend-React_18-61DAFB?logo=react)
![Vite](https://img.shields.io/badge/Bundler-Vite-646CFF?logo=vite)
![Flask](https://img.shields.io/badge/Backend-Flask-000000?logo=flask)

**StudyAI** is an intelligent, context-aware study management platform designed to help students and professionals optimize their learning schedules, track progress, and test their knowledge using state-of-the-art simulated AI features. 

---

## ✨ Advanced Features

### 🤖 Context-Aware AI Assistant
- **Natural Language Processing:** Tell the AI *"add a task to read chapter 5 tomorrow"* and it will automatically extract the context, adjust the deadline, and insert it directly into your planner.
- **Smart Scheduling:** Ask the AI to *"plan my day"* and it will analyze your pending tasks, sort them by urgency and priority, and dynamically generate a personalized Markdown schedule.
- **Instant Insights:** Query the assistant about your subject progress to get immediate overviews of your completed hours and difficulties.

### 📝 AI Document Quiz Generator
- **Smart Parsing:** Upload your lecture notes, PDFs, or textbook chapters, and the system simulates an advanced analysis phase to extract core concepts.
- **Conceptual MCQs:** Generates highly relevant, difficult multiple-choice questions tailored to your document's topic (e.g., Deep Learning, OS threading, Networking) rather than simple fill-in-the-blank queries.
- **Instant Explanations:** Every selected answer provides a deep AI explanation, reinforcing why an option is correct or incorrect.
- **Dynamic Re-generation:** Generate entirely new banks of shuffled questions from the same document without having to re-upload.

### ⏳ Productivity & Analytics
- **Pomodoro Timer:** Built-in focused study timer with customizable intervals.
- **Analytics Dashboard:** Visualize your study habits, task completion rates, and subject focus.
- **Priority Calendar:** Manage your deadlines and view your upcoming week at a glance.

---

## 🚀 Getting Started

### Prerequisites
- Node.js (v18+ recommended)
- Python (3.10+)

### Frontend Setup (React/Vite)
1. Navigate to the project root directory.
2. Install the required Node dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   *The frontend will run on `http://localhost:5173` (or the next available port).*

### Backend Setup (Flask/Python)
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   .\\venv\\Scripts\\activate
   # Mac/Linux
   source venv/bin/activate
   ```
3. Install the Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask server (forcing UTF-8 encoding and port 5001 is recommended):
   ```bash
   # Windows PowerShell
   $env:PYTHONIOENCODING="utf-8"; $env:PORT="5001"; python run.py
   
   # Mac/Linux
   PYTHONIOENCODING="utf-8" PORT=5001 python run.py
   ```
   *The backend API will run on `http://localhost:5001`.*

---

## 🛠 Tech Stack

**Frontend:**
- React 18 (TypeScript)
- Vite for lightning-fast HMR and building
- React Router DOM for seamless SPA routing
- Tailwind CSS & Lucide React for beautiful UI styling

**Backend:**
- Python 3
- Flask (API serving)

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.

## 📝 License

This project is licensed under the MIT License.
