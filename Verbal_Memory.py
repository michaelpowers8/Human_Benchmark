from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from warnings import filterwarnings
from Global import *

def open_verbal_memory(driver:Chrome,logger:Logger) -> None|Exception:
    try:
        # Wait for the play link to be clickable (10 second timeout)
        play_link:WebElement = driver.find_element(By.CSS_SELECTOR, "a[href*='/tests/verbal-memory'] svg[data-icon='play-circle']").find_element(By.XPATH, "..")
        
        sleep(1)
        # Click the link
        play_link.click()
        logger.info("Successfully opened Verbal Memory.")
    except Exception as e:
        logger.critical(f"Verbal Memory failed to open. Terminating program. Official error: {str(e)}")
        raise Exception(f"Error: {e}")
    
def start_verbal_memory(driver:Chrome,logger:Logger) -> None|Exception:
    try:
        # Wait for the start button to be clickable (10 second timeout)
        start_button:WebElement = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'css-de05nr') and contains(@class, 'e19owgy710') and text()='Start']"))
                    )
        
        sleep(1)
        # Click the link
        start_button.click()
        logger.info("Verbal Memory successfully started playing.")
    except Exception as e:
        logger.critical(f"Verbal Memory failed to start playing. Terminating program. Official error: {str(e)}")
        raise Exception(f"Error: {e}")

def play(driver:Chrome,words:list[str],score:int,logger:Logger) -> tuple[list[str],int]|Exception:
    try:
        # Wait for the word container to load
        word_element:WebElement = driver.find_element(By.CSS_SELECTOR, "div.css-1qvtbrk.e19owgy78 div.word")
        if(word_element.text in words):
            # Wait for the button to be clickable and then click it
            try:
                seen_button:WebElement = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'css-de05nr') and contains(@class, 'e19owgy710') and text()='SEEN']"))
                )
                
                seen_button.click()
                score += 1
                
            except Exception as e:
                logger.critical(f"Error clicking the SEEN button. Official Error: {e}. Terminating the program.")
                raise Exception(f"{str(e)}")
        else:
            # Wait for the button to be clickable and then click it
            words.append(word_element.text)
            try:
                new_button:WebElement = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'css-de05nr') and contains(@class, 'e19owgy710') and text()='NEW']"))
                )
                
                new_button.click()
                score += 1
            except Exception as e:
                logger.critical(f"Error clicking the NEW button. Official Error: {e}. Terminating the program.")
                raise Exception(f"{str(e)}")
        return words,score
    except Exception as e:
        logger.critical(f"Exception occurred while playing. Official Error: {str(e)}")
        raise Exception(f"{str(e)}")

if __name__ == "__main__":
    filterwarnings('ignore')
    logger:Logger = create_logger()
    driver:Chrome = load_driver(logger)
    username,password,post_test_delay,visual_memory,\
        verbal_memory,typing,number_memory,\
            reaction_time,sequence_memory,\
                aim_trainer,chimp_test = load_configuration()
    if(not(verbal_memory)):
        logger.info("Verbal Memory in config.json set to false. Terminating program.")
    else:
        words:list[str] = []
        score:int = 0
        driver.get("https://humanbenchmark.com/login")

        input_username(driver,username,logger)
        input_password(driver,password,logger)
        click_login(driver,logger)  
            
        sleep(3) # Wait time to ensure full page loads

        open_verbal_memory(driver,logger)
        start_verbal_memory(driver,logger)
        
        while score < 10_000: # Human benchmark crashes at a score beyond 10,000, so this is the maximum.
            words,score = play(driver,words,score,logger)
            sleep(0.02)
            if(score%1_000==0):
                logger.info(f"Current Verbal Memory Score: {score:,.0f}")

        save_score(driver,logger)

        driver.close()