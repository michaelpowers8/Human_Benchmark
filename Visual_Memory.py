from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from warnings import filterwarnings
from Global import *

def open_visual_memory(driver:Chrome,logger:Logger) -> None|Exception:
    try:
        # Wait for the play link to be clickable (10 second timeout)
        play_link:WebElement = driver.find_element(By.CSS_SELECTOR, "a[href*='/tests/memory']")
        sleep(0.5)
        # Click the link
        play_link.click()
        logger.info("Visual Memory successfully opened.")
    except Exception as e:
        logger.critical(f"Visual Memory failed to open. Terminating program. Official error: {str(e)}")
        raise Exception(f"Error: {e}")
    
def start_visual_memory_game(driver:Chrome,logger:Logger):
    try:
        # Wait for the start button to be clickable (10 second timeout)
        start_button:WebElement = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'css-de05nr') and contains(@class, 'e19owgy710') and text()='Start']"))
                    )
        
        sleep(0.5)
        # Click the link
        start_button.click()
        logger.info("Visual Memory successfully started playing.")
    except Exception as e:
        logger.critical(f"Visual Memory failed to start playing. Terminating program. Official error: {str(e)}")
        raise Exception(f"Error: {e}")

def play(driver:Chrome,logger:Logger) -> None|Exception:
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
        logger.info("Level successfully completed.")
    except Exception as e:
        logger.critical(f"Level failed to complete. Terminating program. Official error: {str(e)}")
        raise Exception(f"Error: {str(e)}")

if __name__ == "__main__":
    filterwarnings('ignore')
    logger:Logger = create_logger()
    driver:Chrome = load_driver(logger)
    username,password,visual_memory,\
        verbal_memory,typing,number_memory,\
            reaction_time,sequence_memory,\
                aim_trainer,chimp_test = load_configuration()
    while True:
        score:int = 0
        driver.get("https://humanbenchmark.com/login")

        input_username(driver,username,logger)
        input_password(driver,password,logger)
        click_login(driver,logger)  
        
        sleep(3)

        open_visual_memory(driver,logger)
        start_visual_memory_game(driver,logger)
                
        while score < 250: # Human benchmar crashes at a score beyond 250, so this is the maximum
            play(driver,logger)
            score += 1
            sleep(1.5)

        logger.info("250 levels completed. ")
        sleep(300) # Here to allow user to manually save because if save_score fails, all time spent accumulating the score will be lost
        
        save_score(driver,logger)