import json
from time import sleep
from logging import basicConfig,Logger,getLogger
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

def create_logger():
    # Create and configure logger
    basicConfig(filename="Human_Benchmark.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    # Creating an object
    logger:Logger = getLogger()
    return logger

def load_configuration() -> tuple[str,str,bool,bool,bool,bool,bool,bool,bool,bool]:
    with open("Config.json","r") as file:
        configuration = json.load(file)
    username:str = configuration["Username"]
    password:str = configuration["Password"]
    visual_memory:bool = configuration["Visual_Memory"]
    verbal_memory:bool = configuration["Verbal_Memory"]
    typing:bool = configuration["Typing"]
    number_memory:bool = configuration["Number_Memory"]
    reaction_time:bool = configuration["Reaction_Time"]
    sequence_memory:bool = configuration["Sequence_Memory"]
    aim_trainer:bool = configuration["Aim_Trainer"]
    chimp_test:bool = configuration["Chimp_Test"]
    return username,password,visual_memory,verbal_memory,typing,number_memory,reaction_time,sequence_memory,aim_trainer,chimp_test

def load_driver(logger:Logger) -> Chrome:
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
    logger.info("Chrome successfully opened")
    return driver

def input_username(driver:Chrome,username:str,logger:Logger) -> None|Exception:
    try:
        # Wait for the element to be present (up to 10 seconds)
        username_field:WebElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='username']"))
        )
        
        # Interact with the field
        username_field.click()          # Focus the field
        username_field.clear()          # Clear existing text (if any)
        username_field.send_keys(username)  # Type your username
        logger.info("Username successfully inputted.")
    except Exception as e:
        logger.critical(f"Username failed to be inputted. Terminating program. Official error: {str(e)}")
        raise Exception(f"Error: {str(e)}")
    
def input_password(driver:Chrome,password:str,logger:Logger) -> None|Exception:
    try:
        # Wait for the element to be present (up to 10 seconds)
        password_field:WebElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
        )
        
        # Interact with the field
        password_field.click()          # Focus the field
        password_field.clear()          # Clear existing text (if any)
        password_field.send_keys(password)  # Type your username
        logger.info("Password successfully inputted.")
    except Exception as e:
        logger.critical(f"Password failed to be inputted. Terminating program. Official error: {str(e)}")
        raise Exception(f"Error: {str(e)}")
    
def click_login(driver:Chrome,logger:Logger) -> None|Exception:
    try:
        # Wait for the element to be present (up to 10 seconds)
        login_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Login']")
        login_button.click()
        logger.info("Login successfully clicked. Opening dashboard")
    except Exception as e:
        logger.critical(f"Login button failed to be clicked. Terminating program. Official error: {str(e)}")
        raise Exception(f"Error: {str(e)}")

def save_score(driver:Chrome,logger:Logger):
    try:
        # Wait for button to be clickable (up to 10 seconds)
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.css-qm6rs9"))
        )
        sleep(1)
        save_button.click()
        logger.info("Score successfully saved.")
    except Exception as e:
        logger.critical(f"Score failed to save. Terminating program. Official error: {str(e)}")
        raise Exception(f"Error: {e}")