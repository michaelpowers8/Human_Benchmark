# <div class="square" style="width: 132px; height: 132px; border-width: 8.25px; border-radius: 16.5px;"></div>
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from warnings import filterwarnings
from Global import *

def play(driver:Chrome,level:int):
    try:
        # Find all square rows
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".square.active"))
        )

        sequence:list[WebElement] = []
        while(len(sequence)<level):
            item:WebElement = driver.find_element(By.CSS_SELECTOR, ".square.active")
            if(len(sequence)==0):
                sequence.append(item)
            elif((len(sequence)>0)and(not(item==sequence[-1]))):
                sequence.append(item)

        sleep(1.25)

        actions:ActionChains = ActionChains(driver)
        for square in sequence:
            actions.click(square).pause(0.05)
        actions.perform()

    except Exception as e:
        logger.critical(f"Level failed to complete. Terminating program. Official error: {str(e)}")
        raise Exception(f"Error: {str(e)}")

if(__name__ == "__main__"):
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
    if(not(sequence_memory)):
        logger.info("Visual Memory set to false in config.json. Terminating program.")
    else:
        try:
            score:int = 0
            driver.get("https://humanbenchmark.com/login")

            input_username(driver,username,logger)
            input_password(driver,password,logger)
            click_login(driver,logger)  

            open_game(driver,logger,'sequence')
            start_game(driver,logger,'sequence')

            while(score<sequence_memory_max_score):
                play(driver,score+1)
                score += 1
        except Exception as e:
            logger.critical(f"Game crashed. Official error: {str(e)}. Terminating the program.")
            raise Exception(f"Game crashed. Official error: {str(e)}. Terminating the program.")