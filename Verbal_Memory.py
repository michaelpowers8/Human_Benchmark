from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from warnings import filterwarnings
from Global import *

def play(driver:Chrome,words:list[str],score:int,logger:Logger) -> tuple[list[str],int]|Exception:
    try:
        # Wait for the word container to load
        word:str = driver.find_element(By.CSS_SELECTOR, "div.css-1qvtbrk.e19owgy78 div.word").text
        if(len(words)>0 and word==words[-1]):
            return words,score
        if(word in words):
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
            words.append(word)
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

def lose(driver:Chrome,words:list[str],score:int,logger:Logger) -> tuple[list[str],int]|Exception:
    try:
        # Wait for the word container to load
        word_element:WebElement = driver.find_element(By.CSS_SELECTOR, "div.css-1qvtbrk.e19owgy78 div.word")
        if(not(word_element.text in words)):
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
        try:
            words:list[str] = []
            score:int = 0
            driver.get("https://humanbenchmark.com/login")

            input_username(driver,username,logger)
            input_password(driver,password,logger)
            click_login(driver,logger)  
                
            sleep(3) # Wait time to ensure full page loads

            open_game(driver,logger,"verbal-memory")
            start_game(driver,logger,"verbal-memory")
            
            while score < 9950: # Human benchmark crashes at a score beyond 10,000, so this is the maximum.
                words,score = play(driver,words,score,logger)
                if(score%500==0):
                    logger.info(f"Current Verbal Memory Score: {score:,.0f}")

            for _ in range(3):
                words,score = lose(driver,words,score,logger)

            sleep(post_test_delay)
            save_score(driver,logger)

            driver.close()
        except Exception as e:
            logger.critical(f"Game crashed. Official error: {str(e)}. Terminating the program.")
            raise Exception(f"Game crashed. Official error: {str(e)}. Terminating the program.")