import time
import pandas as pd 
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CommentsScraper():

    def __init__(self, user_path):
        self.PATH = user_path

    def commentsToDataFrame(self, video_link, num_of_comments, initial_wait = 15, sleep_time = 2):

        """Function to scrape comments off of a YouTube video and 
        return it in the form of a dataframe.
        
        Args: 
            video_link (string): link of the YouTube video
            num_of_comments (int): number of comments to be scraped
            initial_wait (int): initial waiting time
            sleep_time (int): sleeping period (in seconds)
        
        Returns: 
            pandas DataFrame: a pandas DataFrame consisting of the scraped comments
    
        """

        data=[]

        with Chrome(self.PATH) as driver:
            wait = WebDriverWait(driver, initial_wait)
            driver.get(video_link)

            for item in range(num_of_comments): 
                wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
                time.sleep(sleep_time)

            for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content-text"))):
                data.append(comment.text)
          
        df = pd.DataFrame(data, columns=['comment'])
        
        return df

