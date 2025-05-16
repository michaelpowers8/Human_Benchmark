from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from warnings import filterwarnings

def load_driver() -> Chrome:
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
    return driver

def input_username(driver:Chrome,username:str) -> None|Exception:
    try:
        # Wait for the element to be present (up to 10 seconds)
        username_field:WebElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='username']"))
        )
        
        # Interact with the field
        username_field.click()          # Focus the field
        username_field.clear()          # Clear existing text (if any)
        username_field.send_keys(username)  # Type your username
    except Exception as e:
        raise Exception(f"Error: {str(e)}")
    
def input_password(driver:Chrome,password:str) -> None|Exception:
    try:
        # Wait for the element to be present (up to 10 seconds)
        password_field:WebElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
        )
        
        # Interact with the field
        password_field.click()          # Focus the field
        password_field.clear()          # Clear existing text (if any)
        password_field.send_keys(password)  # Type your username
        return
    except Exception as e:
        raise Exception(f"Error: {str(e)}")
    
def click_login(driver:Chrome) -> None|Exception:
    try:
        # Wait for the element to be present (up to 10 seconds)
        login_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Login']")
        login_button.click()
        return  
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def open_visual_memory(driver:Chrome) -> None|Exception:
    try:
        # Wait for the play link to be clickable (10 second timeout)
        play_link:WebElement = driver.find_element(By.CSS_SELECTOR, "a[href*='/tests/memory']")
        sleep(0.5)
        # Click the link
        play_link.click()
    except Exception as e:
        raise Exception(f"Error: {e}")
    
def start_visual_memory_game(driver:Chrome):
    try:
        # Wait for the start button to be clickable (10 second timeout)
        start_button:WebElement = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'css-de05nr') and contains(@class, 'e19owgy710') and text()='Start']"))
                    )
        
        sleep(0.5)
        # Click the link
        start_button.click()
    except Exception as e:
        print(f"Error: {e}")

def play(driver:Chrome) -> None|Exception:
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
            for square in active_squares:                
                if(current_square.location == square.location):
                    current_square.click()
                    active_squares.remove(square)
                    break
        return
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

if __name__ == "__main__":
    filterwarnings('ignore')
    driver:Chrome = load_driver()
    while True:
        score:int = 0
        driver.get("https://humanbenchmark.com/login")

        input_username(driver,"micpowers98@gmail.com")
        input_password(driver,"Idnarb10!!")
        click_login(driver)  
        sleep(3)

        open_visual_memory(driver)
        start_visual_memory_game(driver)
                
        while score < 100:
            play(driver)
            score += 1
            sleep(1.5)

        sleep(1_000_000)
        
        try:
            # Wait for button to be clickable (up to 10 seconds)
            save_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.css-qm6rs9"))
            )
            save_button.click()
        except Exception as e:
            print(f"Error: {e}")