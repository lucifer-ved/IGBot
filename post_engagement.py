import time
import re
import random
from config import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PostEngagement:

    def __init__(self, username, passwd):
        self.username = username
        self.passwd = passwd
        self.driver = webdriver.Firefox()
        self.driver.set_window_size(800,800)

    def login(self):        
        driver = self.driver
        driver.get(URL)
        self.sleep_for_sometime()
        user_name = driver.find_element_by_xpath(USERNAME_ELEMENT)
        user_name.clear()
        self.add_input(user_name,self.username)
        # user_name.send_keys(self.username)
        password = driver.find_element_by_xpath(PASSWORD_ELEMENT)
        password.clear()
        self.add_input(password,self.passwd)
        # password.send_keys(self.passwd)
        password.send_keys(Keys.RETURN)
        self.sleep_for_sometime()
        try:
            not_now = driver.find_element_by_xpath(NOT_NOW_ELEMENT)
            not_now.click()
            self.sleep_for_sometime(5)
            not_now = driver.find_element_by_xpath(NOT_NOW_ELEMENT)
            not_now.click()
            self.sleep_for_sometime(5)
        except Exception as e:
            pass


    def get_pictures_for_specific_hashtag(self,hashtag,scroll=3):
        search_element = self.driver.find_element_by_xpath(SEARCHBAR_ELEMENT)
        self.add_input(search_element,hashtag)
        self.sleep_for_sometime(7)
        search_element.send_keys(Keys.RETURN)
        self.sleep_for_sometime(7)
        search_element.send_keys(Keys.RETURN)
        # self.driver.get(HASHTAG_URL.format(hashtag))
        self.sleep_for_sometime()

        images_hrefs = []
        for i in range(1,scroll):
            try:
                self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                self.sleep_for_sometime()
                #get hrefs elements of all post in view
                hrefs_in_current_window = self.driver.find_elements_by_tag_name(ANCHOR_TAG)
                #get only hrefs from elements
                hrefs_in_current_window = [elem.get_attribute(HREF_TAG) for elem in hrefs_in_current_window]
                #filterout required hrefs
                [images_hrefs.append(href) for href in hrefs_in_current_window if href not in UNWANTED_URLS]
            except Exception:
                continue
        return images_hrefs

    def write_comment(self,comment):
        try:
            self.sleep_for_sometime(4)
            comment_textarea  = self.driver.find_element_by_xpath(COMMENT_TEXT_AREA)
            comment_textarea.click()
            self.add_input(comment_textarea,comment)
        except Exception as e:
            if(e.__class__. __name__ == 'StaleElementReferenceException'):
                print('StaleElementReferenceException while trying to type comment, trying to find element again')
                comment_textarea  = self.driver.find_element_by_xpath(COMMENT_TEXT_AREA)
                comment_textarea.click()
                comment_textarea.send_keys('')
                comment_textarea.clear()
            else:
                print("No such element as 'Comment'")
        self.add_input(comment_textarea,comment)
        # comment_textarea.send_keys(Keys.RETURN)

    def like_post(self):
        try:
            like_button_container = self.driver.find_element_by_class_name(LIKE_BUTTON_CLASS_NAME)
            like_button = like_button_container.find_element_by_xpath(LIKE_ICON)
            # like_icon.click()
        except Exception as e:
            print("No Such Element as 'Like'")

    def clickon_picture_for_specific_hashtag(self,image_list):
        for image in image_list:
            self.driver.get(image)
            self.sleep_for_sometime(4)
            self.like_post()
            self.write_comment("This book is really good!")

    def add_input(self,input_element,text):
        for letter in text:
            input_element.send_keys(letter)            
            self.sleep_for_sometime((random.randint(1,7)/30))

    def close_browser(self):
        self.driver.close()

    def sleep_for_sometime(self,sec=4):
        time.sleep(sec)


postObj = PostEngagement(username=USERNAME,passwd=PASSWORD)
postObj.login()
image_list = postObj.get_pictures_for_specific_hashtag('#booklover')
postObj.clickon_picture_for_specific_hashtag(image_list)

    
