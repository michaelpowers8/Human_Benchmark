from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from warnings import filterwarnings
from Global import *

def play(driver:Chrome,logger:Logger,level_number:int,lose:bool) -> None|Exception:
    try:
        # Wait for at least one active square to appear
        big_number:str = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "big-number")
            )
        ).text

        # Wait for the input element to be present and interactable
        input_element:WebElement = WebDriverWait(driver, 10+(level_number*3)).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[pattern='[0-9]*'][type='text']"))
        )
        if(lose):
            input_element.send_keys("231879374293928383109201804820140749275927536972832981")
        else:
            input_element.send_keys(big_number)

        # Wait for the start button to be clickable (10 second timeout)
        submit_button:WebElement = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'css-de05nr') and contains(@class, 'e19owgy710') and text()='Submit']"))
                    )
        submit_button.click()

        if(lose):
            return None
        # Wait for the start button to be clickable (10 second timeout)
        next_button:WebElement = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'css-de05nr') and contains(@class, 'e19owgy710') and text()='NEXT']"))
                    )
        next_button.click()

        logger.info(f"Level {level_number:,.0f} -> {big_number} successfully completed.")
    except Exception as e:
        logger.critical(f"Level failed to complete. Terminating program. Official error: {str(e)}")
        raise Exception(f"Error: {str(e)}")

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
    if(not(number_memory)):
        logger.info("Visual Memory set to false in config.json. Terminating program.")
    else:
        score:int = 0
        driver.get("https://humanbenchmark.com/login")

        input_username(driver,username,logger)
        input_password(driver,password,logger)
        click_login(driver,logger)  

        open_game(driver,logger,"number-memory")
        start_game(driver,logger,"number-memory")

        while(score < 98):
            play(driver,logger,score+1,False)
            score += 1
        play(driver,logger,score+1,True)
        
        save_score()