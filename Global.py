import json
from time import sleep
from logging import Logger,getLogger,FileHandler,Formatter
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime

def create_logger() -> Logger:
    logger:Logger = getLogger("HumanBenchmark")
    logger.setLevel("INFO")  # Ensure it captures INFO and higher
    # Only add handlers if none exist (avoid duplicate logs)
    if not logger.handlers:
        current_day:datetime = datetime.now().strftime("%Y%m%d")
        file_handler = FileHandler(f"Human_Benchmark_{current_day}.log", mode="a")
        formatter = Formatter('%(asctime)s %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger

def load_configuration() -> tuple[str,str,int|float,bool,bool,bool,bool,bool,bool,bool,bool]:
    with open("Config.json","r") as file:
        configuration = json.load(file)
    username:str = configuration["Username"]
    password:str = configuration["Password"]
    post_test_delay:int|float = configuration["Post_Test_Score_Delay"]
    visual_memory:bool = configuration["Visual_Memory"][0]
    visual_memory_max_score:int = configuration["Visual_Memory"][1]
    verbal_memory:bool = configuration["Verbal_Memory"][0]
    verbal_memory_max_score:int = configuration["Verbal_Memory"][1]
    typing:bool = configuration["Typing"][0]
    typing_min_score:int = configuration["Typing"][1]
    number_memory:bool = configuration["Number_Memory"][0]
    number_memory_max_score:int = configuration["Number_Memory"][1]
    reaction_time:bool = configuration["Reaction_Time"][0]
    reaction_time_max_score:int = configuration["Reaction_Time"][1]
    sequence_memory:bool = configuration["Sequence_Memory"][0]
    sequence_memory_max_score:bool = configuration["Sequence_Memory"][1]
    aim_trainer:bool = configuration["Aim_Trainer"][0]
    chimp_test:bool = configuration["Chimp_Test"][0]
    return username,password,post_test_delay,\
        visual_memory,visual_memory_max_score,\
            verbal_memory,verbal_memory_max_score,\
                typing,typing_min_score,\
                    number_memory,number_memory_max_score,\
                        reaction_time,reaction_time_max_score,\
                            sequence_memory,sequence_memory_max_score,\
                                aim_trainer,chimp_test

def load_driver(logger:Logger) -> Chrome:
    # WebDriver Chrome
    options = ChromeOptions()
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
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-ipc-flooding-protection")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver:Chrome = Chrome(options=options)
    driver.get("https://humanbenchmark.com/login")
    logger.info("Chrome successfully opened")
    return driver

def input_username(driver:Chrome,username:str,logger:Logger) -> None|Exception:
    try:
        # Wait for the element to be present (up to 10 seconds)
        username_field:WebElement = WebDriverWait(driver, 15).until(
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
        password_field:WebElement = WebDriverWait(driver, 15).until(
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
        login_button = WebDriverWait(driver, 15).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH, "//input[@type='submit' and @value='Login']")
                                )
                            )
        
        login_button.click()
        logger.info("Login successfully clicked. Opening dashboard")
    except Exception as e:
        logger.critical(f"Login button failed to be clicked. Terminating program. Official error: {str(e)}")
        raise Exception(f"Error: {str(e)}")

def login_to_human_benchmark(driver:Chrome,username:str,password:str,logger:Logger):
    input_username(driver,username,logger)
    input_password(driver,password,logger)
    click_login(driver,logger)  

def open_game(driver:Chrome,logger:Logger,game:str) -> None|Exception:
    try:
        # Wait for the play link to be clickable (10 second timeout)
        play_link:WebElement = WebDriverWait(driver, 15).until(
                                EC.element_to_be_clickable(
                                    (By.CSS_SELECTOR, f"a[href*='/tests/{game}'] svg[data-icon='play-circle']")
                                )
                            )
        
        play_link.click()
        logger.info(f"Successfully opened {game.replace("-"," ").title()}.")
    except Exception as e:
        logger.critical(f"{game.replace("-"," ").title()} failed to open. Terminating program. Official error: {str(e)}")
        raise Exception(f"Error: {e}")
    
def start_game(driver:Chrome,logger:Logger,game:str) -> None|Exception:
    try:
        # Wait for the start button to be clickable (10 second timeout)
        start_button:WebElement = WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'css-de05nr') and contains(@class, 'e19owgy710') and text()='Start']"))
                    )
        
        start_button.click()
        logger.info(f"{game.replace("-"," ").title()} successfully started playing.")
    except Exception as e:
        logger.critical(f"{game.replace("-"," ").title()} failed to start playing. Terminating program. Official error: {str(e)}")
        raise Exception(f"Error: {e}")

def save_score(driver:Chrome,logger:Logger,max_retries:int=5) -> None|Exception:
    for attempt in range(max_retries):
        try:
            # Wait for button to be clickable (up to 10 seconds)
            save_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.css-qm6rs9"))
            )
            save_button.click()
            logger.info("Score successfully saved.")
            return
        except Exception as e:
            if(attempt<4):
                logger.error(f"Score failed to save. Retrying to save. Official error: {str(e)}")
            else:
                logger.critical(f"Too many failed save score attempts. Terminating program. Official error: {str(e)}")
                raise Exception(f"Error: {e}")