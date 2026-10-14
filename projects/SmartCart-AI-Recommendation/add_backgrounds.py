def inject_backgrounds():
    # 1. Update base.html CSS
    with open('templates/base.html', 'r', encoding='utf-8') as f:
        base = f.read()
        
    # Replace the body style
    old_body = """body { 
            font-family: 'Plus Jakarta Sans', sans-serif; 
            background-color: var(--background); 
            color: var(--text-main);
            padding-top: 80px;
        }"""
    
    new_body = """body { 
            font-family: 'Plus Jakarta Sans', sans-serif; 
            background-image: url('https://images.unsplash.com/photo-1557682250-33bd709cbe85?w=1600&q=80');
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
            color: var(--text-main);
            padding-top: 80px;
        }
        /* Add a semi-transparent overlay over the entire body for readability */
        body::before {
            content: '';
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(243, 244, 246, 0.85); /* Light overlay */
            z-index: -1;
        }"""
    
    base = base.replace(old_body, new_body)
    
    # Replace the hero-banner style
    old_hero = """/* Hero Section */
        .hero-banner {
            background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
            border-radius: 30px;
            padding: 80px 40px;
            text-align: center;
            box-shadow: 0 20px 40px rgba(79, 70, 229, 0.1);
            margin-bottom: 60px;
            position: relative;
            overflow: hidden;
        }
        .hero-banner::before { content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 70%); animation: rotate 20s linear infinite; }
        @keyframes rotate { 100% { transform: rotate(360deg); } }
        .hero-title { font-weight: 800; font-size: 3.5rem; color: #1E3A8A; position: relative; z-index: 1; letter-spacing: -1px; }
        .hero-subtitle { font-size: 1.2rem; color: #4F46E5; font-weight: 500; margin-bottom: 30px; position: relative; z-index: 1; }"""
        
    new_hero = """/* Hero Section */
        .hero-banner {
            background-image: url('https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?w=1600&q=80');
            background-size: cover;
            background-position: center;
            border-radius: 30px;
            padding: 100px 40px;
            text-align: center;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
            margin-bottom: 60px;
            position: relative;
            overflow: hidden;
        }
        .hero-banner::before { 
            content: ''; 
            position: absolute; 
            top: 0; left: 0; width: 100%; height: 100%; 
            background: linear-gradient(135deg, rgba(79, 70, 229, 0.85) 0%, rgba(17, 24, 39, 0.9) 100%);
        }
        .hero-title { font-weight: 800; font-size: 4rem; color: #ffffff; position: relative; z-index: 1; letter-spacing: -1px; text-shadow: 0 4px 12px rgba(0,0,0,0.3); }
        .hero-subtitle { font-size: 1.3rem; color: #E0E7FF; font-weight: 400; margin-bottom: 35px; position: relative; z-index: 1; }"""
        
    base = base.replace(old_hero, new_hero)
    
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(base)
        
    print("Backgrounds successfully injected!")

if __name__ == '__main__':
    inject_backgrounds()
