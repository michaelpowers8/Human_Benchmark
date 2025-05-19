from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from warnings import filterwarnings
from Global import *

def click_seen_new_button(driver:Chrome,button_string:str,score:int) -> int:
    # Wait for the button to be clickable and then click it
    try:
        button:WebElement = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'css-de05nr') and contains(@class, 'e19owgy710') and text()='{button_string}']"))
        )
        
        button.click()
        score += 1
        return score
    except Exception as e:
        logger.critical(f"Error clicking the SEEN button. Official Error: {e}. Terminating the program.")
        raise Exception(f"{str(e)}")

def play(driver:Chrome,words:list[str],score:int,logger:Logger) -> tuple[list[str],int]|Exception:
    try:
        # Wait for the word container to load
        word:str = driver.find_element(By.CSS_SELECTOR, "div.css-1qvtbrk.e19owgy78 div.word").text
        if(word in words):
            score = click_seen_new_button(driver,'SEEN',score)
        else:
            # Wait for the button to be clickable and then click it
            words.append(word)
            score = click_seen_new_button(driver,'NEW',score)
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
            score = click_seen_new_button(driver,'SEEN',score)
        else:
            # Wait for the button to be clickable and then click it
            words.append(word_element.text)
            score = click_seen_new_button(driver,'NEW',score)
        return words,score
    except Exception as e:
        logger.critical(f"Exception occurred while playing. Official Error: {str(e)}")
        raise Exception(f"{str(e)}")

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
    if(not(verbal_memory)):
        logger.info("Verbal Memory in Config.json set to false. Terminating program.")
    else:
        words:list[str] = []
        score:int = 0
        driver.get("https://humanbenchmark.com/login")

        input_username(driver,username,logger)
        input_password(driver,password,logger)
        click_login(driver,logger)  

        open_game(driver,logger,"verbal-memory")
        start_game(driver,logger,"verbal-memory")
        
        while score < verbal_memory_max_score: # Human benchmark crashes at a score beyond 10,000, so this is the maximum.
            words,score = play(driver,words,score,logger)
            if(score%500==0):
                logger.info(f"Current Verbal Memory Score: {score:,.0f}")

        for _ in range(3):
            words,score = lose(driver,words,score,logger)

        sleep(post_test_delay)
        save_score(driver,logger)

        driver.close()