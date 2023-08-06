from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from browsercmd.page import google
import shutil
import browsercmd.common.utils as utils
import json
from random import randint
import time
import sys
import os
import traceback
class Google():
    profile_tmp_download="tmp"
    email=""
    ip_email = "http://178.128.211.227"
    def __init__(self,driver, email, pass_word, reco_email):
        self.driver = driver
        self.retries_upload = 3
        self.email = email
        self.pass_word = pass_word
        self.reco_email = reco_email

    def login(self):
        self.driver.get("https://www.youtube.com/upload?approve_browser_access=1")
        login_page=google.LoginPage(self.driver)
        if login_page.is_login():
            try:
                login_page.change_language()
            except:
                pass
            try:
                login_page.click_profile_indentifier()
            except:
                pass
            try:
                login_page.email_login = self.email+Keys.RETURN
                time.sleep(1)
            except:
                pass
            try:
                login_page.pass_word_login = self.pass_word+Keys.RETURN
                time.sleep(3)
            except:
                pass
            try:
               # pos = imagesearch(ImageResource.RECOVERY_MAIL)
                #click_image(ImageResource.RECOVERY_MAIL, pos, "left", 1)
                login_page.click_cofirm_reco(self.reco_email)
            except:
                #print(traceback.format_exc())
                pass
            try:
                login_page.click_done_button()
            except:
                pass
            try:
                login_page.click_confirm_button()
            except:
                pass
            time.sleep(5)
            self.driver.get("https://www.youtube.com/upload?approve_browser_access=1")
            login_page = google.LoginPage(self.driver)
            if login_page.is_login():
                print("Login  Fail")
                utils.call_error(self.url_cb_log, self.job_id, self.email, "6;;Login fail")
                return False
        return True
    def close(self):
        utils.save_cookie(self.ip_email,self.cookie_cur_folder,self.email)
        self.driver.close()
        self.driver.quit()
        shutil.rmtree(self.cookie_load_folder)
    def finish(self):
        utils.unlock_process(self.url_cb_log, self.job_id)
        cmd = "vncserver -kill :77"
        os.popen(cmd).read()
    def changeName(self):
        if not self.new_full_name and self.new_full_name != "None":
            self.driver.get("https://aboutme.google.com/#name")
            time.sleep(5)
            aboutPage = google.AboutMePage(self.driver)
            aboutPage.change_name(self.new_full_name)

