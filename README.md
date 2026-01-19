# 🎮 The Hacker Store - Insecure Deserialization Project
**Author:** Bar Lahat  
**Vulnerability:** Python Pickle Insecure Deserialization  
**Impact:** Logic Manipulation (Cheating) & Remote Code Execution (RCE via Web Shell)

## 📌 Project Overview
This project demonstrates a critical web vulnerability: **Insecure Deserialization**.
We simulate a game store where user state is serialized insecurely using Python's `pickle` module.

The project demonstrates two attack vectors and a comprehensive fix:
1.  **Logic Exploit:** Modifying serialized objects to gain **Infinite Money** and **Admin Privileges**.
2.  **RCE Exploit:** Injecting a malicious payload to plant a permanent **Web Shell** (Backdoor) on the server.
3.  **Secure Implementation:** A patched version using **JSON** and **HMAC Signatures**.

## 📂 File Structure
* `vulnerable_game.py`: The vulnerable Flask application (The Store). Uses `pickle`.
* `secure_game.py`: The secured Flask application. Uses `json` + `HMAC`.
* `exploit_cheat.py`: Generates a payload to modify user stats (Coins/Admin).
* `exploit_backdoor.py`: Generates a payload that uses PowerShell to drop a `shell.html` backdoor.

## 🚀 How to Run the Demo

### Part 1: Logic Attack (The Cheat)
1.  Run the vulnerable server:
    ```bash
    python vulnerable_game.py
    ```
2.  Visit `http://127.0.0.1:5000`. You are a "Guest" with 10 coins.
3.  Run `python exploit_cheat.py`, copy the cookie, inject it, and refresh.
4.  **Result:** You are now Admin, have 1,000,000 coins, and the Flag is unlocked.

### Part 2: RCE Attack (The Web Shell)
1.  Ensure `vulnerable_game.py` is running.
2.  Run `python exploit_backdoor.py`, copy the cookie, inject it, and refresh.
3.  Navigate to the secret backdoor: `http://127.0.0.1:5000/page/shell.html`
4.  **Result:** You have full command execution access. Try running `dir` or `whoami`.

### Part 3: The Fix (Secure Server)
1.  Stop the vulnerable server and run the secure one:
    ```bash
    python secure_game.py
    ```
2.  Visit `http://127.0.0.1:5001` (Note: Port 5001).
3.  Try injecting the payloads from Part 1 or Part 2.
4.  **Result:** The server detects the invalid signature/format, rejects the cookie, and resets you to a safe "Guest" profile.

## 🛡️ Mitigation Strategy
To fix Insecure Deserialization, we applied two layers of defense in `secure_game.py`:
1.  **Format Change (JSON):** We replaced `pickle` (which executes code) with `json` (which handles data only). This eliminates the RCE vulnerability.
2.  **Integrity Check (HMAC):** We added a cryptographic signature (HMAC-SHA256) to the cookie. If a user modifies their coins/level, the signature mismatch causes the server to reject the data.

---
*For Educational Purposes Only.*