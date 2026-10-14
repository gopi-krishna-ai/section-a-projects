import os

base_dir = r'C:\Users\krish\OneDrive\Desktop\section a\01_GuardPath_AI_Updated\B-1-GuardPath AI\static\css'
style_path = os.path.join(base_dir, 'style.css')

css_content = """@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --primary: #0f172a;        /* Slate 900 */
    --primary-light: #334155;  /* Slate 700 */
    --accent: #2563eb;         /* Blue 600 */
    --accent-hover: #1d4ed8;   /* Blue 700 */
    --safe: #10b981;           /* Emerald 500 */
    --moderate: #f59e0b;       /* Amber 500 */
    --unsafe: #ef4444;         /* Red 500 */
    --text: #1e293b;           /* Slate 800 */
    --muted: #64748b;          /* Slate 500 */
    --border: rgba(226, 232, 240, 0.6);
    --shadow-soft: 0 8px 32px rgba(15, 23, 42, 0.08);
    --shadow-glow: 0 8px 20px rgba(37, 99, 235, 0.25);
    --glass-bg: rgba(255, 255, 255, 0.75);
}

* { box-sizing: border-box; }

body {
    margin: 0;
    font-family: 'Inter', sans-serif;
    color: var(--text);
    min-height: 100vh;
    background: url('https://images.unsplash.com/photo-1524661135-423995f22d0b?q=80&w=1920&auto=format&fit=crop') fixed center/cover;
}

/* FROSTED GLASS OVERLAY */
body::before {
    content: '';
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(135deg, rgba(241, 245, 249, 0.85) 0%, rgba(226, 232, 240, 0.95) 100%);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    z-index: -1;
}

/* TOPBAR (Glassmorphism) */
.topbar {
    background: rgba(15, 23, 42, 0.9);
    backdrop-filter: blur(16px);
    color: white;
    padding: 16px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.brand { display: flex; align-items: center; gap: 14px; }
.brand-icon { font-size: 30px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));}
.brand h1 { margin: 0; font-size: 24px; font-weight: 800; letter-spacing: -0.5px; background: linear-gradient(to right, #fff, #93c5fd); -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
.tagline { margin: 2px 0 0; font-size: 13px; color: #94a3b8; font-weight: 500;}

.topbar a { transition: all 0.2s; font-weight: 600; padding: 6px 12px; border-radius: 6px;}
.topbar a:hover { background: rgba(255,255,255,0.1); }

/* CONTAINER & PANELS */
.container {
    max-width: 1050px;
    margin: 50px auto;
    padding: 0 20px;
    animation: fadeIn 0.5s ease-out;
}
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

.panel {
    background: var(--glass-bg);
    border-radius: 24px;
    padding: 35px;
    box-shadow: var(--shadow-soft);
    margin-bottom: 35px;
    border: 1px solid rgba(255, 255, 255, 1);
    backdrop-filter: blur(10px);
}

.panel h2 { 
    margin-top: 0; 
    font-size: 24px; 
    font-weight: 800; 
    margin-bottom: 28px; 
    background: linear-gradient(135deg, var(--primary), #475569);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}

/* FORMS & INPUTS */
.field-row {
    display: flex;
    gap: 24px;
    margin-bottom: 24px;
    flex-wrap: wrap;
}

.field { flex: 1; min-width: 220px; display: flex; flex-direction: column; gap: 8px; }
.field label { font-size: 13px; font-weight: 700; color: var(--primary-light); text-transform: uppercase; letter-spacing: 0.5px;}

select, input[type="text"], input[type="password"] {
    padding: 14px 18px;
    border: 1px solid rgba(203, 213, 225, 0.8);
    border-radius: 12px;
    font-size: 15px;
    background: rgba(255, 255, 255, 0.6);
    color: var(--text);
    transition: all 0.3s ease;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
}
select:focus, input:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.15);
    background: #ffffff;
}

.toggle-group { 
    display: flex; 
    background: rgba(255,255,255,0.6); 
    border-radius: 12px; 
    overflow: hidden; 
    width: fit-content; 
    padding: 6px;
    border: 1px solid rgba(203, 213, 225, 0.8);
}
.toggle-btn {
    padding: 10px 24px;
    border: none;
    background: transparent;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    color: var(--muted);
    border-radius: 8px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.toggle-btn.active { 
    background: #ffffff; 
    color: var(--accent); 
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.submit-btn, .btn-login {
    margin-top: 15px;
    width: 100%;
    padding: 16px 28px;
    border: none;
    border-radius: 14px;
    background: linear-gradient(135deg, var(--accent) 0%, #1e40af 100%);
    color: white;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 0.5px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-glow);
}
.submit-btn:hover, .btn-login:hover { 
    transform: translateY(-2px); 
    box-shadow: 0 12px 24px rgba(37, 99, 235, 0.35); 
}
.submit-btn:active, .btn-login:active { transform: translateY(0); box-shadow: var(--shadow-glow); }

.form-error { color: var(--unsafe); font-size: 14px; margin-top: 12px; min-height: 20px; font-weight: 600; background: #fee2e2; padding: 10px; border-radius: 8px; border: 1px solid #f87171; display: none;}
.form-error:not(:empty) { display: block; }
.loading { text-align: center; color: var(--accent); padding: 20px; font-weight: 700; font-size: 18px;}

/* MAP STYLING */
.map-wrap {
    height: 550px;
    width: 100%;
    border-radius: 16px;
    overflow: hidden;
    position: relative;
    border: 4px solid #ffffff;
    box-shadow: var(--shadow-soft);
}
#route-map { height: 100%; width: 100%; }

.map-heading-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 20px;
}
.map-note { font-size: 14px; color: var(--muted); max-width: 650px; line-height: 1.6; margin-top: 8px; }
.map-status {
    background: var(--safe);
    color: white;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3);
}

.map-overlay-card {
    position: absolute;
    bottom: 24px;
    right: 24px;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(12px);
    padding: 16px 20px;
    border-radius: 16px;
    box-shadow: var(--shadow-soft);
    z-index: 1000;
    font-size: 13px;
    font-weight: 600;
    display: flex;
    flex-direction: column;
    gap: 10px;
    border: 1px solid rgba(255,255,255,1);
}
.traffic-dot, .danger-dot {
    display: inline-block;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    margin-right: 8px;
}
.traffic-dot.low { background: var(--safe); }
.traffic-dot.medium { background: var(--moderate); }
.traffic-dot.high { background: var(--unsafe); }
.danger-dot { background: var(--unsafe); border: 2px solid white; box-shadow: 0 0 0 1px var(--unsafe); }

.map-hint { font-size: 15px; color: var(--primary-light); font-weight: 600; margin-top: 20px; text-align: center; background: rgba(255,255,255,0.6); padding: 10px; border-radius: 8px;}

.map-controls {
    display: flex;
    gap: 16px;
    margin-top: 24px;
    justify-content: center;
    align-items: center;
}
.secondary-btn {
    padding: 12px 24px;
    border: 1px solid var(--border);
    border-radius: 10px;
    background: #fff;
    color: var(--primary-light);
    font-size: 14px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
.secondary-btn:hover:not(:disabled) { background: #f8fafc; color: var(--accent); border-color: var(--accent); }
.secondary-btn:disabled { opacity: 0.5; cursor: not-allowed; box-shadow: none; }
.trip-progress { font-size: 15px; color: var(--primary); font-weight: 700; margin-left: 10px; background: white; padding: 10px 16px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.05);}

/* ROUTE RESULTS STYLING */
.results-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
}
.route-card {
    border: 1px solid rgba(255,255,255,0.8);
    border-radius: 16px;
    padding: 24px;
    background: rgba(255,255,255,0.6);
    transition: all 0.3s ease;
}
.route-card:hover {
    background: #fff;
    box-shadow: var(--shadow-soft);
    transform: translateY(-2px);
}
.route-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 16px;
}
.route-card-header h3 { margin: 0; font-size: 20px; color: var(--primary); display: flex; align-items: center; gap: 10px; font-weight: 800;}
.route-badge {
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.route-badge.safe { background: #d1fae5; color: #065f46; border: 1px solid #34d399;}
.route-badge.moderate { background: #fef3c7; color: #92400e; border: 1px solid #fbbf24;}
.route-badge.unsafe { background: #fee2e2; color: #991b1b; border: 1px solid #f87171;}

.route-score-box { text-align: right; }
.route-score-val { font-size: 28px; font-weight: 800; letter-spacing: -1px;}
.route-score-box.safe { color: var(--safe); }
.route-score-box.moderate { color: var(--moderate); }
.route-score-box.unsafe { color: var(--unsafe); }

.route-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 16px;
    margin-bottom: 20px;
}
.stat-box {
    background: rgba(255,255,255,0.8);
    padding: 16px;
    border-radius: 12px;
    border: 1px solid var(--border);
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
}
.stat-box small { display: block; color: var(--muted); font-size: 12px; font-weight: 700; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;}
.stat-box strong { font-size: 16px; color: var(--primary); font-weight: 800;}

.route-reasons { margin: 0; padding-left: 24px; color: var(--primary-light); font-size: 15px; line-height: 1.6; font-weight: 500;}
.route-reasons li { margin-bottom: 8px; }

/* CUSTOM PAGE STYLES (LANDING & LOGIN) */
.hero { text-align: center; padding: 60px 20px; }
.hero h1 { font-size: 3.5rem; margin-bottom: 24px; background: linear-gradient(135deg, var(--primary), var(--accent)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; letter-spacing: -1.5px; }
.hero p { font-size: 1.25rem; color: var(--primary-light); max-width: 750px; margin: 0 auto 50px auto; line-height: 1.8; font-weight: 500;}
.steps { display: flex; justify-content: center; gap: 30px; margin-bottom: 60px; flex-wrap: wrap; }
.step-card {
    background: rgba(255, 255, 255, 0.8);
    padding: 35px 25px;
    border-radius: 20px;
    box-shadow: var(--shadow-soft);
    width: 300px;
    text-align: center;
    border: 1px solid rgba(255,255,255,1);
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}
.step-card:hover { transform: translateY(-8px); box-shadow: var(--shadow-glow); border-color: rgba(37, 99, 235, 0.3);}
.step-card h3 { color: var(--accent); margin-bottom: 16px; font-size: 22px; font-weight: 800; letter-spacing: -0.5px;}
.step-card p { color: var(--muted); font-size: 16px; line-height: 1.6; font-weight: 500;}

.btn-login {
    display: inline-block;
    width: auto;
    padding: 18px 48px;
    border-radius: 30px;
    font-size: 18px;
}

/* HISTORY TABLE */
.table { width: 100%; border-collapse: separate; border-spacing: 0; margin-top: 24px; border-radius: 12px; overflow: hidden; border: 1px solid var(--border); box-shadow: 0 4px 12px rgba(0,0,0,0.03);}
.table th, .table td { padding: 18px 24px; text-align: left; border-bottom: 1px solid var(--border); }
.table th { background: #f8fafc; color: var(--primary); font-weight: 700; font-size: 13px; text-transform: uppercase; letter-spacing: 1px;}
.table td { background: rgba(255,255,255,0.8); font-size: 15px; color: var(--text); font-weight: 500;}
.table tr:last-child td { border-bottom: none; }
.table tr:hover td { background: #ffffff; }

/* BADGES */
.badge { padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; color: white; display: inline-block; letter-spacing: 0.5px;}
.badge.safe { background: var(--safe); box-shadow: 0 2px 6px rgba(16,185,129,0.3);}
.badge.short { background: var(--moderate); box-shadow: 0 2px 6px rgba(245,158,11,0.3);}

/* LOGIN & HISTORY UTILS */
.nav-links { margin-top: 10px; display: flex; gap: 24px; margin-bottom: 30px; }
.nav-links a { text-decoration: none; color: var(--primary-light); font-weight: 700; transition: all 0.2s; background: rgba(255,255,255,0.6); padding: 10px 20px; border-radius: 10px; border: 1px solid var(--border);}
.nav-links a:hover { color: var(--accent); background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.05); transform: translateY(-1px);}
.alert { background: #fee2e2; color: #991b1b; padding: 14px; border-radius: 10px; text-align: center; margin-bottom: 24px; font-weight: 600; border: 1px solid #f87171;}
.test-credentials { margin-top: 30px; padding: 24px; background: rgba(255,255,255,0.5); border-radius: 12px; border: 1px solid var(--border); font-size: 15px; color: var(--primary-light); font-weight: 500;}
.test-credentials code { background: white; padding: 4px 8px; border-radius: 6px; border: 1px solid var(--border); font-family: 'Courier New', Courier, monospace; color: var(--accent); font-weight: 700; box-shadow: 0 2px 4px rgba(0,0,0,0.02);}

/* FOOTER */
.footer { text-align: center; padding: 30px; color: var(--muted); font-size: 14px; font-weight: 500;}
"""

with open(style_path, 'w', encoding='utf-8') as f:
    f.write(css_content)

print("Updated style.css with premium UI.")
