# Human Benchmark Automation with Selenium

## Overview

This project demonstrates the capabilities of Selenium WebDriver for browser automation by interacting with the Human Benchmark cognitive testing platform. The scripts are designed for educational purposes to study Selenium's efficiency in a consistent web environment, not for cheating on leaderboards.

## Features

- **Multiple Test Automation**:
  - Visual Memory
  - Verbal Memory
  - Typing Test
  - Number Memory
- **Configurable Settings** via `Config.json`
- **Detailed Logging** with timestamps
- **Headless Mode Support** (commented out)
- **Anti-Detection Measures** to avoid bot detection

## Prerequisites

- Python 3.x
- Chrome browser
- ChromeDriver (matching your Chrome version)
- Required Python packages:
  ```
  selenium
  pyautogui
  ```

## Configuration

Edit `Config.json` to set your preferences:

```json
{
  "Username": "your_username",
  "Password": "your_password",
  "Post_Test_Score_Delay": 2,
  "Visual_Memory": true,
  "Verbal_Memory": true,
  "Typing": true,
  "Number_Memory": true,
  "Reaction_Time": false,
  "Sequence_Memory": false,
  "Aim_Trainer": false,
  "Chimp_Test": false
}
```

## How to Run

1. Clone the repository
2. Install dependencies: `pip install selenium pyautogui`
3. Configure `Config.json` with your credentials
4. Run individual test scripts:
   ```
   python Visual_Memory.py
   python Verbal_Memory.py
   python Typing.py
   python Number_Memory.py
   ```

## Important Notes

- This project is for **educational purposes only**
- The scripts include intentional delays to mimic human behavior
- High scores are artificially generated to test system limits
- The project demonstrates web automation techniques, not legitimate testing strategies

## Disclaimer

This automation script is provided for educational purposes to demonstrate Selenium capabilities. The author does not condone using this to gain unfair advantages on the Human Benchmark platform. Users are responsible for their own actions and should respect platform terms of service.

## License

This project is open-source and available for educational use. Commercial use or misuse is prohibited.