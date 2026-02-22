import os
import logging
from flask import Flask, session, render_template_string, request

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "MySuperSecretKey_DoNotShare")

# --- הגדרת לוגר אבטחה ייעודי (Dedicated Security Logger) ---
security_logger = logging.getLogger('security_audit')
security_logger.setLevel(logging.INFO)

# יצירת קובץ הלוג
file_handler = logging.FileHandler('security.log')
# הגדרת הפורמט רק עבור הלוגר הזה
formatter = logging.Formatter('%(asctime)s [%(levelname)s] IP: %(client_ip)s | %(message)s')
file_handler.setFormatter(formatter)

# הוספת ה-Handler ללוגר
security_logger.addHandler(file_handler)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Store - Fixed Logs</title>
    <style>
        body { font-family: 'Courier New', monospace; background-color: #0d1117; color: #c9d1d9; text-align: center; padding: 50px; }
        .card { border: 2px solid #2ea043; padding: 20px; display: inline-block; background-color: #161b22; border-radius: 10px; min-width: 400px; }
        h1 { color: #2ea043; }
        .stats { color: #79c0ff; font-size: 18px; margin-bottom: 20px; border-bottom: 1px solid #30363d; padding-bottom: 15px; text-align: left; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🛡️ SECURE SYSTEM 🛡️</h1>
        <div class="stats">
            👤 USER: <b>{{ player.username }}</b><br>
            💰 COINS: {{ player.coins }}<br>
            🛡️ ADMIN: {{ '✅ YES' if player.is_admin else '❌ NO' }}
        </div>
    </div>
</body>
</html>
"""


@app.route('/')
def home():
    client_ip = request.remote_addr

    # משתמשים ב-security_logger במקום ב-logging הכללי
    if 'username' not in session:
        security_logger.info("New session started", extra={'client_ip': client_ip})
        session['username'] = "Guest_User"
        session['coins'] = 10
        session['is_admin'] = False
    else:
        security_logger.info(f"Page refresh: {session['username']}", extra={'client_ip': client_ip})

    return render_template_string(HTML_TEMPLATE, player=session)


@app.route('/admin-panel')
def admin_panel():
    client_ip = request.remote_addr
    # כאן אנחנו משתמשים ב-security_logger עם רמת ERROR
    security_logger.error("UNAUTHORIZED ACCESS ATTEMPT to /admin-panel", extra={'client_ip': client_ip})
    return "ACCESS DENIED. Logged.", 403


if __name__ == '__main__':
    print("[*] Server running. Security logs are separated.")
    app.run(host='0.0.0.0', port=5001)