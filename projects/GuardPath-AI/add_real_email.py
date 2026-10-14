import os
import re

base_dir = r'C:\Users\krish\OneDrive\Desktop\section a\01_GuardPath_AI_Updated\B-1-GuardPath AI'
app_path = os.path.join(base_dir, 'app.py')

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

email_imports = '''import smtplib
from email.message import EmailMessage

# --- EMAIL CONFIGURATION ---
# To send REAL emails, replace these with your Gmail address and a Google App Password
SENDER_EMAIL = 'your_email@gmail.com'
SENDER_PASSWORD = 'your_app_password'

def send_real_email(to_email, subject, body):
    if SENDER_EMAIL == 'your_email@gmail.com':
        print("Real email skipped: Please configure SENDER_EMAIL in app.py")
        return False
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = f"GuardPath AI <{SENDER_EMAIL}>"
        msg['To'] = to_email

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email failed: {e}")
        return False
'''

# Find a good place to inject the email logic (after imports)
content = content.replace("from werkzeug.utils import secure_filename", "from werkzeug.utils import secure_filename\n\n" + email_imports)

old_sos_send = '''    # Simulate sending Email
    print(f"\\n{'='*40}\\n🚨 URGENT SOS EMAIL SENT 🚨\\nTo: {email}\\nFrom: GuardPath Safety System\\nUser: {alert['name']}\\nLocation: LAT {lat}, LNG {lng}\\nMessage: {message}\\n{'='*40}\\n")'''

new_sos_send = '''    # Attempt to send REAL Email
    email_body = f"""🚨 URGENT SOS EMERGENCY ALERT 🚨
    
User '{alert['name']}' has triggered an SOS.

📍 Live Location: LAT {lat}, LNG {lng}
https://maps.google.com/?q={lat},{lng}

✉️ Custom Message:
{message}

Please respond immediately.
- GuardPath AI Safety System"""

    email_sent = send_real_email(email, "🚨 URGENT SOS ALERT from GuardPath AI", email_body)
    
    if email_sent:
        print(f"REAL Email successfully sent to {email}")
    else:
        print(f"\\n{'='*40}\\n🚨 SIMULATED SOS EMAIL 🚨\\nTo: {email}\\n{email_body}\\n{'='*40}\\n")'''

content = content.replace(old_sos_send, new_sos_send)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app.py with real email logic")
