from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from warnings import filterwarnings
from Global import *

def play(driver:Chrome,logger:Logger,level_number:int) -> None|Exception:
    try:
        # Wait for at least one active square to appear
        active_squares:list[WebElement] = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.active.css-lxtdud.eut2yre1:not(.error)")
            )
        )
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.active.css-lxtdud"))
        )
        current_squares:list[WebElement] = driver.find_elements(By.CSS_SELECTOR, "div.css-lxtdud.eut2yre1")
        for current_square in current_squares:
            for square in active_squares:                
                if(current_square.location == square.location):
                    current_square.click()
                    active_squares.remove(square)
                    break
        logger.info(f"Level {level_number:,.0f} successfully completed.")
    except Exception as e:
        logger.critical(f"Level failed to complete. Terminating program. Official error: {str(e)}")
        raise Exception(f"Error: {str(e)}")

if __name__ == "__main__":
    filterwarnings('ignore')
    logger:Logger = create_logger()
    driver:Chrome = load_driver(logger)
    username,password,post_test_delay,visual_memory,\
        verbal_memory,typing,number_memory,\
            reaction_time,sequence_memory,\
                aim_trainer,chimp_test = load_configuration()
    if(not(visual_memory)):
        logger.info("Visual Memory set to false in config.json. Terminating program.")
    else:
        try:
            score:int = 0
            driver.get("https://humanbenchmark.com/login")

            input_username(driver,username,logger)
            input_password(driver,password,logger)
            click_login(driver,logger)  

            open_game(driver,logger,'memory')
            start_game(driver,logger,'visual-memory')
                    
            while score < 250: # Human benchmark crashes at a score beyond 250, so this is the maximum
                play(driver,logger,score+1)
                score += 1
                sleep(1.5) # Time between when level ends and new level of blocks is revealed for player to memorize
                if(score%25==0):
                    logger.info(f"Current Visual Memory Score: {score:,.0f}")

            logger.info("250 levels completed. Saving score and terminating the program")
            sleep(post_test_delay) # Here to allow user to manually save because if save_score fails, all time spent accumulating the score will be lost
            
            save_score(driver,logger)
            driver.close()
        except Exception as e:
            logger.critical(f"Game crashed. Official error: {str(e)}. Terminating the program.")
            raise Exception(f"Game crashed. Official error: {str(e)}. Terminating the program.")