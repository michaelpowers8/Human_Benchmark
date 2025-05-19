from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from warnings import filterwarnings
from Global import *
from pyautogui import typewrite,PAUSE
from random import uniform

def play(driver:Chrome,logger:Logger) -> None|Exception:
    try:
        # Wait for the letters container to load
        letters_container:WebElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "letters"))
        )
        logger.info("Letter container found.")
        
        # Extract all character spans
        character_spans:list[WebElement] = letters_container.find_elements(By.TAG_NAME, "span")
        logger.info("Character spans created.")
        
        # Create a list of characters (including spaces and punctuation)
        characters:list[str] = [span.text if len(span.text)>0 else " " for span in character_spans]
        logger.info("List of characters created from span.")
        message:str = "".join(characters)
        logger.info(f"Message created: {message}")

        # Click the typing area to focus it
        typing_area:WebElement = driver.find_element(By.CLASS_NAME, "letters")
        typing_area.click()
        logger.info("Typing area found and clicked")

        #typing_area.send_keys(message)
        typewrite(message,interval=uniform(0.1,0.2))
        logger.info("Typing test successfully completed.")
        return None
    except Exception as e:
        logger.critical(f"Typing test failed. Official Error: {str(e)}. Terminating program.")
        raise Exception(f"Typing test failed. Official Error: {str(e)}. Terminating program.")
    
def analyze_wpm_results(driver:Chrome,logger:Logger,min_score:int) -> bool|Exception:
    try:
        # Wait for the WPM element to load
        wpm_element:WebElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.css-0"))
        )
        
        # Extract the text (e.g., "15553wpm")
        wpm_text:str = wpm_element.text
        
        # Extract only the numeric part using string manipulation
        wpm_number = ''.join(filter(str.isdigit, wpm_text))  # "15553"
        # OR (if the format is consistent)
        wpm_number = wpm_text.replace("wpm", "")  # "15553"
        if(wpm_number.isdigit()):
            wpm_number = int(wpm_number)
        save:bool = False
        if(isinstance(wpm_number,int) and wpm_number>=min_score):
            save:bool = True
        logger.info(f"Words per minute successfully analyzed. Typing speed of {wpm_number:,.0f} {'will' if save else 'will not'} be saved.")
        return save
    except Exception as e:
        logger.critical(f"Failed to analyze words per minute. Official error: {str(e)}. Terminating program.")
        raise Exception(f"Failed to analyze words per minute. Official error: {str(e)}. Terminating program.")

if __name__ == "__main__":
    filterwarnings('ignore')
    logger:Logger = create_logger()
    driver:Chrome = load_driver(logger)
    username,password,post_test_delay,\
        visual_memory,visual_memory_max_score,\
            verbal_memory,verbal_memory_max_score,\
                typing,typing_min_score,\
                    number_memory,number_memory_max_score,\
                        reaction_time,reaction_time_max_score,\
                            sequence_memory,sequence_memory_max_score,\
                                aim_trainer,chimp_test = load_configuration()
    if(not(typing)):
        logger.info("Typing in config.json set to false. Terminating program.")
    else:
        driver.get("https://humanbenchmark.com/login")

        input_username(driver,username,logger)
        input_password(driver,password,logger)
        click_login(driver,logger)  

        open_game(driver,logger,"typing")
        play(driver,logger)
        
        sleep(post_test_delay)
        save:bool = analyze_wpm_results(driver,logger,typing_min_score)
        if(save):
            save_score(driver,logger)

        driver.close()