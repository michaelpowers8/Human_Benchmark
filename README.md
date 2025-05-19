# HumanBenchmark Automation (Educational Use Only)

This repository contains Python scripts that demonstrate the use of Selenium WebDriver to automate interactions with [humanbenchmark.com](https://humanbenchmark.com). **These scripts are strictly for educational purposes** and should not be used to manipulate leaderboards or disrupt the platform.

---

## ⚠️ Disclaimer
This project is intended **only for learning purposes**:
- Demonstrates Selenium WebDriver automation techniques.
- Shows how to interact with dynamic web elements (login forms, games, etc.).
- Includes error handling and logging best practices.

**Do not use this to spam or cheat on humanbenchmark.com.** Respect the platform's terms of service.

---

## 📦 Included Scripts
| Script               | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `Global.py`          | Shared utilities (logger, driver setup, login functions).                   |
| `Visual_Memory.py`   | Automates the Visual Memory test (matches highlighted squares).             |
| `Verbal_Memory.py`   | Plays the Verbal Memory game (identifies repeated words).                  |
| `Typing.py`          | Completes the typing test using `pyautogui` for realistic input.            |
| `Number_Memory.py`   | Solves the Number Memory challenge (recalls increasingly long numbers).     |
| `Sequence_Memory.py` | Repeats highlighted square sequences in the Sequence Memory test.           |

---

## ⚙️ Configuration
1. **Edit `Config.json`** to set:
   - Login credentials (username/password).
   - Enable/disable specific tests.
   - Adjust target scores for each game.

Example `Config.json`:
```json
{
  "Username": "my-username@example.com",
  "Password": "my-password",
  "Post_Test_Score_Delay": 2.0,
  "Visual_Memory": [true, 50],
  "Verbal_Memory": [true, 100],
  "Typing": [true, 80],
  "Number_Memory": [true, 15],
  "Reaction_Time": [false, 0],
  "Sequence_Memory": [true, 30],
  "Aim_Trainer": [false],
  "Chimp_Test": [false]
}