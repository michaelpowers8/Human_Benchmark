# HumanBenchmark Automation

This project automates various tests on the HumanBenchmark website (https://humanbenchmark.com) using Selenium WebDriver. The scripts can perform tests like Visual Memory, Verbal Memory, Number Memory, and Typing with configurable settings.

## Features

- Automated testing for multiple HumanBenchmark games:
  - Visual Memory
  - Verbal Memory
  - Number Memory
  - Typing
- Configurable through `Config.json`
- Detailed logging of all operations
- Headless browser option available

## Requirements

- Python 3.x
- Selenium
- ChromeDriver (matching your Chrome version)
- PyAutoGUI (for Typing test)
- Google Chrome browser

## Installation

1. Clone this repository
2. Install required packages:
   ```
   pip install selenium pyautogui
   ```
3. Download ChromeDriver from https://sites.google.com/chromium.org/driver/ and ensure it's in your PATH

## Configuration

Edit the `Config.json` file to set your preferences:

```json
{
  "Username": "my-username@example.com",
  "Password": "my-password",
  "Post_Test_Score_Delay": 3,
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

## Usage

Run individual test scripts:

- `Visual_Memory.py`
- `Verbal_Memory.py`
- `Number_Memory.py`
- `Typing.py`

Each script will:
1. Log in to HumanBenchmark using your credentials
2. Navigate to the specified test
3. Perform the test according to its logic
4. Save the score (if configured to do so)

## Notes

- The scripts include intentional "lose" conditions to make scores appear more natural
- Some tests have maximum score limits to prevent website crashes
- Logs are saved daily with timestamps in `Human_Benchmark_YYYYMMDD.log`
- For the typing test, extremely high WPM scores (≥15000) will trigger an automatic save

## Disclaimer

This project is for educational purposes only. Please use responsibly and in accordance with HumanBenchmark's terms of service. The authors are not responsible for any account restrictions that may result from using this automation.