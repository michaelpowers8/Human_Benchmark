from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyautogui import typewrite
from time import sleep

if __name__ == "__main__":
    # WebDriver Chrome
    options = ChromeOptions()
    #options.add_argument('--headless=new')
    # adding argument to disable the AutomationControlled flag 
    options.add_argument("--disable-blink-features=AutomationControlled") 
    # exclude the collection of enable-automation switches 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    # turn-off userAutomationExtension 
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument('--disable-extensions')
    options.add_argument('--profile-directory=Default')
    options.add_argument("--incognito")
    options.add_argument("--disable-plugins-discovery")
    options.add_argument("--start-maximized")

    driver:Chrome = Chrome(options=options)

    while True:
        driver.get("https://humanbenchmark.com/login")

        try:
            # Wait for the element to be present (up to 10 seconds)
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='username']"))
            )
            
            # Interact with the field
            username_field.click()          # Focus the field
            username_field.clear()          # Clear existing text (if any)
            username_field.send_keys("micpowers98@gmail.com")  # Type your username
            
            print("Successfully entered username!")
        except Exception as e:
            print(f"Error: {e}")

        try:
            # Wait for the element to be present (up to 10 seconds)
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
            )
            
            # Interact with the field
            password_field.click()          # Focus the field
            password_field.clear()          # Clear existing text (if any)
            password_field.send_keys("Idnarb10!!")  # Type your username
            
            print("Successfully entered password!") 
        except Exception as e:
            print(f"Error: {e}")

        try:
            # Wait for the element to be present (up to 10 seconds)
            login_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Login']")
            login_button.click()
            
            print("Successfully logged in!")    
        except Exception as e:
            print(f"Error: {e}")

        sleep(3)

        try:
            # Wait for the play link to be clickable (10 second timeout)
            play_link = driver.find_element(By.CSS_SELECTOR, "a[href*='/tests/typing'] svg[data-icon='play-circle']").find_element(By.XPATH, "..")
            
            sleep(1)
            # Click the link
            play_link.click()
            print("Successfully clicked Play button")
        except Exception as e:
            print(f"Error: {e}")

        try:
            # Wait for the letters container to load
            letters_container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "letters"))
            )

            # Click the typing area to focus it
            typing_area = driver.find_element(By.CLASS_NAME, "letters")
            typing_area.click()
            
            # Extract all character spans
            character_spans = letters_container.find_elements(By.TAG_NAME, "span")
            
            # Create a list of characters (including spaces and punctuation)
            characters = [span.text if len(span.text)>0 else " " for span in character_spans]
            
            typewrite("".join(characters))
        except Exception as e:
            print(str(e))

        try:
            # Wait for the WPM element to load
            wpm_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.css-0"))
            )
            
            # Extract the text (e.g., "15553wpm")
            wpm_text = wpm_element.text
            
            # Extract only the numeric part using string manipulation
            wpm_number = ''.join(filter(str.isdigit, wpm_text))  # "15553"
            # OR (if the format is consistent)
            wpm_number = wpm_text.replace("wpm", "")  # "15553"
            if(wpm_number.isdigit()):
                wpm_number = int(wpm_number)
            save = False
            if(isinstance(wpm_number,int) and wpm_number>=25000):
                save = True
        except Exception as e:
            print(f"Error: {e}")
        
        try:
            # Wait for button to be clickable (up to 10 seconds)
            save_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.css-qm6rs9"))
            )
            
            # Click the button
            if(save):
                save_button.click()
                print("Successfully clicked 'Save score'")
            else:
                print("Score too low.")
        except Exception as e:
            print(f"Error: {e}")