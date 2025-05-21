from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from warnings import filterwarnings
from Global import *

def build_sequence(driver:Chrome,size_of_sequence:int,logger:Logger) -> list[WebElement]:
    try:
        sequence:list[WebElement] = []
        while(len(sequence)<size_of_sequence):
            item:WebElement = driver.find_element(By.CSS_SELECTOR, ".square.active")
            if(len(sequence)==0): # Checking for any ac
                sequence.append(item)
            elif((len(sequence)>0)and(not(item==sequence[-1]))):
                sequence.append(item)
        return sequence
    except Exception as e:
        logger.critical(f"Failed to build the sequence. Terminating program. Official error: {str(e)}")
        raise Exception(f"Error: {str(e)}")

def repeat_sequence(driver:Chrome,sequence:list[WebElement],logger:Logger) -> None:
    try:
        actions:ActionChains = ActionChains(driver)
        for square in sequence:
            actions.click(square).pause(0.1)
        actions.perform()
        return None
    except Exception as e:
        logger.critical(f"Failed to repeat the sequence. Terminating program. Official error: {str(e)}")
        raise Exception(f"Error: {str(e)}")

def play(driver:Chrome,level:int,logger:Logger):
    # Find all square rows
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".square.active"))
    )
    sequence:list[WebElement] = build_sequence(driver,size_of_sequence=level,logger=logger)
    sleep(1.25) # Delay to ensure the sequence is ready to be repeated in the memory game
    repeat_sequence(driver,sequence,logger)

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
    del post_test_delay,visual_memory,visual_memory_max_score,verbal_memory,verbal_memory_max_score,typing,typing_min_score,number_memory,number_memory_max_score,reaction_time,reaction_time_max_score,aim_trainer,chimp_test
    if(not(sequence_memory)):
        logger.info("Visual Memory set to false in config.json. Terminating program.")
    else:
        score:int = 0
        login_to_human_benchmark(driver,username,password,logger) 

        open_game(driver,logger,'sequence')
        start_game(driver,logger,'sequence')

        while(score<sequence_memory_max_score): # Implement a max score that can be configred in Config.json.
            play(driver,score+1,logger)
            sleep(0.25) # Delay between last square in sequence being clicked and start of next sequence being built
            score += 1

if __name__ == "__main__":
    main()