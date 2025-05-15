from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from warnings import filterwarnings

if __name__ == "__main__":
    filterwarnings('ignore')

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
        words:list[str] = []
        score:int = 0
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
            play_link = driver.find_element(By.CSS_SELECTOR, "a[href*='/tests/verbal-memory'] svg[data-icon='play-circle']").find_element(By.XPATH, "..")
            
            sleep(1)
            # Click the link
            play_link.click()
            print("Successfully clicked Play button")
        except Exception as e:
            print(f"Error: {e}")

        try:
            # Wait for the start button to be clickable (10 second timeout)
            start_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'css-de05nr') and contains(@class, 'e19owgy710') and text()='Start']"))
                        )
            
            sleep(1)
            # Click the link
            start_button.click()
            print("Successfully clicked Play button")
        except Exception as e:
            print(f"Error: {e}")

        while score < 10_000:
            try:
                # Wait for the word container to load
                word_element = driver.find_element(By.CSS_SELECTOR, "div.css-1qvtbrk.e19owgy78 div.word")
                if(word_element.text in words):
                    # Wait for the button to be clickable and then click it
                    try:
                        seen_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'css-de05nr') and contains(@class, 'e19owgy710') and text()='SEEN']"))
                        )
                        
                        seen_button.click()
                        score += 1
                        
                    except Exception as e:
                        print(f"Error clicking the button: {e}")
                else:
                    # Wait for the button to be clickable and then click it
                    words.append(word_element.text)
                    try:
                        new_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'css-de05nr') and contains(@class, 'e19owgy710') and text()='NEW']"))
                        )
                        
                        new_button.click()
                        score += 1
                        
                    except Exception as e:
                        print(f"Error clicking the button: {e}")
                
            except Exception as e:
                print(str(e))
            
            sleep(0.02)
        
        try:
            # Wait for button to be clickable (up to 10 seconds)
            save_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.css-qm6rs9"))
            )
            save_button.click()
        except Exception as e:
            print(f"Error: {e}")