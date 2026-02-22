import pickle
import base64
import os
from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)

class Player:
    def __init__(self, username):
        self.username = username
        self.level = 1
        self.coins = 10
        self.is_admin = False

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>The Hacker Store</title>
    <style>
        body { font-family: 'Courier New', monospace; background-color: #0d1117; color: #c9d1d9; text-align: center; padding: 50px; }
        .card { border: 1px solid #30363d; padding: 20px; display: inline-block; background-color: #161b22; border-radius: 10px; min-width: 400px; }
        h1 { color: #58a6ff; }
        .stats { color: #79c0ff; font-size: 18px; margin-bottom: 20px; border-bottom: 1px solid #30363d; padding-bottom: 15px; text-align: left; }
    </style>
</head>
<body>
    <div class="card">
        <h1>👾 Player Profile 👾</h1>
        <div class="stats">
            👤 USER: <b>{{ player.username }}</b><br>
            ⭐ LVL: {{ player.level }}<br>
            💰 COINS: {{ player.coins }}<br>
            🛡️ ADMIN: {{ '✅ YES' if player.is_admin else '❌ NO' }}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    user_cookie = request.cookies.get('game_session')
    player = None

    if user_cookie:
        try:
            data = base64.b64decode(user_cookie)
            player = pickle.loads(data)
        except Exception as e:
            # === הוספנו את ההדפסה הזו כדי לראות מה נכשל ===
            print(f"[DEBUG] CRASH: {e}")

    if not player:
        player = Player("Guest_Noob")
        serialized = pickle.dumps(player)
        cookie_val = base64.b64encode(serialized).decode()
        resp = make_response(render_template_string(HTML_TEMPLATE, player=player))
        resp.set_cookie('game_session', cookie_val)
        return resp

    return render_template_string(HTML_TEMPLATE, player=player)

if __name__ == '__main__':
    # מריץ על כל הכתובות כדי שתוכל לגשת גם מהטלפון אם תרצה
    app.run(host='0.0.0.0', port=5000)