from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from warnings import filterwarnings
from Global import *

def get_big_number(driver:Chrome,logger:Logger) -> str: 
    try:
        # Wait for at least one active square to appear
        return WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "big-number")
            )
        ).text
    except Exception as e:
        logger.critical(f"Failed to get the big number. Terminating program. Official error: {str(e)}")
        raise Exception(f"Error: {str(e)}")
    
def input_answer(driver:Chrome,level_number:int,big_number:str,lose:bool,logger:Logger) -> None:
    try:
        # Wait for the input element to be present and interactable
        input_element:WebElement = WebDriverWait(driver, 10+(level_number*3)).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[pattern='[0-9]*'][type='text']"))
        )
        if(lose):
            input_element.send_keys(f"1{big_number}") # Adding an extra 1 to the start of the big number to ensure incorrect number of digits 
        else:
            input_element.send_keys(big_number)
    except Exception as e:
        logger.critical(f"Failed to input the big number. Terminating program. Official error: {str(e)}")
        raise Exception(f"Error: {str(e)}")
    
def submit_answer(driver:Chrome,logger:Logger) -> None:
    try:
          # Wait for the start button to be clickable (10 second timeout)
        submit_button:WebElement = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'css-de05nr') and contains(@class, 'e19owgy710') and text()='Submit']"))
                    )
        submit_button.click()
    except Exception as e:
        logger.critical(f"Failed to submit the answer. Terminating program. Official error: {str(e)}")
        raise Exception(f"Error: {str(e)}")
    
def click_next_level(driver:Chrome,logger:Logger) -> None:
    try:
        # Wait for the start button to be clickable (10 second timeout)
        next_button:WebElement = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'css-de05nr') and contains(@class, 'e19owgy710') and text()='NEXT']"))
                    )
        next_button.click()
    except Exception as e:
        print(e)
        print(str(e))
        logger.critical(f"Failed to move to the next level. Terminating program. Official error: {str(e)}")
        raise Exception(f"Error: {str(e)}")

def play(driver:Chrome,logger:Logger,level_number:int,lose:bool) -> None:
        big_number:str = get_big_number(driver,logger)
        input_answer(driver,level_number,big_number,lose,logger)
        submit_answer(driver,logger)
        if(lose):
            logger.info(f"Level {level_number:,.0f} -> {big_number} successfully lost on purpose.")
            return None
        else:
            click_next_level(driver,logger)
            logger.info(f"Level {level_number:,.0f} -> {big_number} successfully completed.")

def main():
    filterwarnings('always')
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
    del post_test_delay,visual_memory,visual_memory_max_score,verbal_memory,verbal_memory_max_score,typing,typing_min_score,sequence_memory,sequence_memory_max_score,reaction_time,reaction_time_max_score,aim_trainer,chimp_test
    if(not(number_memory)):
        logger.info("Visual Memory set to false in config.json. Terminating program.")
    else:
        score:int = 0
        login_to_human_benchmark(driver,username,password,logger)

        open_game(driver,logger,"number-memory")
        start_game(driver,logger,"number-memory")

        while(score < number_memory_max_score): # Implement a max score that can be configred in Config.json.
            play(driver,logger,score+1,False)
            score += 1
        play(driver,logger,score+1,True)
        
        save_score(driver,logger)

if __name__ == "__main__":
    main()