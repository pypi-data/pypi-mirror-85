from . import BasePage
from browsercmd.elements.google import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
from browsercmd.common.config import ImageResource
from random import randint
class LoginPage(BasePage):
    email_login=EmailLoginElement()
    pass_word_login=PassWordLoginElement()
    email_reco_login=EmailRecoElement()
    email_reco_login2=EmailRecoElement2()
    def is_login(self):
        return "accounts.google.com" in self.driver.current_url
    def is_en_lang(self):
        return "English" in self.driver.find_element(*LoginPageLocators.LANG_CHOOSE_BUTTON).text
    def click_cofirm_reco(self, email_reco):
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.find_element(
                    *LoginPageLocators.RECO_EMAIL_BUTTON))
            self.driver.find_element(*LoginPageLocators.RECO_EMAIL_BUTTON).click()
        except:
            pass
        try:
            self.email_reco_login2 = email_reco + Keys.RETURN
        except:
            pass
        try:
            self.email_reco_login = email_reco + Keys.RETURN
        except:
            pass
    def click_profile_indentifier(self):
        self.driver.find_element(*LoginPageLocators.PROFILE_INDENTIFIER).click()
        time.sleep(2)
    def change_language(self):
        if self.is_en_lang():
            return
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element(
                *LoginPageLocators.LANG_CHOOSE_BUTTON))
        self.driver.find_element(*LoginPageLocators.LANG_CHOOSE_BUTTON).click()
        time.sleep(1)
        self.driver.find_element(*LoginPageLocators.LANG_IT).click()
        time.sleep(2)
        self.driver.find_element(*LoginPageLocators.LANG_CHOOSE_BUTTON).click()
        time.sleep(1)
        self.driver.find_element(*LoginPageLocators.LANG_EN).click()
        time.sleep(2)
    def click_done_button(self):
        self.driver.find_element(*LoginPageLocators.DONE_BUTTON).click()
        time.sleep(2)
    def click_confirm_button(self):
        self.driver.find_element(*LoginPageLocators.CONFIRM_BUTTON).click()
        time.sleep(2)
class SearchResultsPage(BasePage):
    """Search results page action methods come here"""

    def is_results_found(self):
        # Probably should search for this text in the specific page
        # element, but as for now it works fine
        return "No results found." not in self.driver.page_source

class AboutMePage(BasePage):
    def fill_text(self, element, text):
        element = self.driver.find_element(*element)
        element.clear()
        element.send_keys(text)
    def change_name(self, full_name):
        first_name=full_name.split(" ")[0]
        last_name=full_name.split(" ")[1]
        try:
            self.fill_text(AboutMeLocators.FIRST_NAME, first_name)
            time.sleep(1)
            self.fill_text(AboutMeLocators.LAST_NAME, last_name)
        except:
            pass
        time.sleep(1)
        try:
            self.fill_text(AboutMeLocators.SUR_NAME, last_name)
        except:
            pass
        time.sleep(1)
        try:
            self.fill_text(AboutMeLocators.FULL_NAME, full_name)
        except:
            pass
        time.sleep(1)
        try:
            self.fill_text(AboutMeLocators.FIRST_NAME_ROLE, first_name)
            time.sleep(1)
            self.fill_text(AboutMeLocators.LAST_NAME_ROLE, last_name)
        except:
            pass
        time.sleep(1)
        try:
            self.driver.find_element(AboutMeLocators.OK_BUTTON).click()
            time.sleep(3)
            self.driver.find_element(AboutMeLocators.CONFIRM_BUTTON).click()
        except:
            pass