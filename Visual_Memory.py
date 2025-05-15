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
            play_link = driver.find_element(By.CSS_SELECTOR, "a[href*='/tests/memory']")#.find_element(By.XPATH, "..")

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
        except Exception as e:
            print(f"Error: {e}")

        while score < 100:
            try:
                # Wait for at least one active square to appear
                active_squares = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "div.active.css-lxtdud.eut2yre1:not(.error)")
                    )
                )
                sleep(3.5)
                current_squares = driver.find_elements(By.CSS_SELECTOR, "div.css-lxtdud.eut2yre1")
                for current_square in current_squares:
                    for index,square in enumerate(active_squares):                
                        if(current_square.location == square.location):
                            current_square.click()
                            active_squares.remove(square)
                            break
            except Exception as e:
                print(str(e))
            sleep(1.5)

        sleep(5)
        
        try:
            # Wait for button to be clickable (up to 10 seconds)
            save_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.css-qm6rs9"))
            )
            save_button.click()
        except Exception as e:
            print(f"Error: {e}")