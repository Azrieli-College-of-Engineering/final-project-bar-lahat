# 👾 The Hacker Store - Insecure Deserialization Project

**Author:** Bar Lahat  
**Vulnerability:** Python Pickle Insecure Deserialization  
**Impact:** Logic Manipulation (Cheating) & Remote Code Execution (RCE via Route Injection)

---

## 📝 Project Overview
This project demonstrates a critical web vulnerability: **Insecure Deserialization**.

In the simulation, we have a game store where the user's state (coins, admin status) is stored in a cookie. Because the server uses Python's `pickle` module to read this cookie, it is vulnerable to attackers who can manipulate the data or even execute arbitrary code on the server.



---

## 📂 File Structure

* **`vulnerable_game.py`**: The Flask application containing the vulnerability. It trusts the `game_session` cookie blindly using `pickle.loads()`.
* **`secure_game.py`**: The patched version. It uses Flask's encrypted session and features a dedicated `security_audit` logger.
* **`exploit_cheat.py`**: A script that generates a malicious cookie to grant the user 1,000,000 coins and Admin privileges.
* **`exploit_terminal.py`**: A sophisticated RCE exploit that injects a hidden terminal route (`/_t`) directly into the running Flask app memory.

---

## 🚀 How to Run the Demo

### Part 1: Logic Attack (The Cheat)
1.  **Run the vulnerable server:**
    ```bash
    python vulnerable_game.py
    ```
2.  Visit `http://127.0.0.1:5000`. You start as a "Guest_Noob" with 10 coins.
3.  Run `python exploit_cheat.py`. Copy the generated Base64 string.
4.  Replace your `game_session` cookie in the browser and refresh.
    * **Result:** You are now **Master_Hacker** with 1,000,000 coins and **Admin: ✅ YES**.

### Part 2: RCE Attack (Flask Route Injection)
1.  Ensure `vulnerable_game.py` is running.
2.  Run `python exploit_terminal.py` and copy the malicious cookie.
3.  Inject the cookie into your browser and refresh the home page (this triggers the injection in the server's memory).
4.  Navigate to the hidden terminal: `http://127.0.0.1:5000/_t`.
    * **Result:** You now have a **Micro Terminal** on the server. Try running commands like `whoami` or `dir`.

### Part 3: The Fix & Security Auditing
1.  Stop the vulnerable server and run the secure one:
    ```bash
    python secure_game.py
    ```
2.  Visit `http://127.0.0.1:5001`. The server now uses cryptographically signed sessions.
3.  Try to access the honeypot: `http://127.0.0.1:5001/admin-panel`.
    * **Result:** Access is denied (403), and the attempt is logged with your IP address in `security.log`.

---

## 🛡️ Mitigation Strategy
In `secure_game.py`, we implemented a **"Defense in Depth"** approach:

* **Safe Serialization:** We replaced `pickle` with Flask's built-in session, which uses `itsdangerous` to sign data. It cannot be used to execute code.
* **Integrity Checking:** Any attempt to modify the cookie results in a signature mismatch, and Flask will simply ignore the session.
* **Security Logging:** We created a dedicated `security_logger` that records every new session, page refresh, and unauthorized access attempt into a persistent log file for auditing.
=======
