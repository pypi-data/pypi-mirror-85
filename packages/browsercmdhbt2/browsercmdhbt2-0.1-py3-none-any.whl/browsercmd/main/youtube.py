from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from browsercmd.page import youtube
from browsercmd.locators.youtube import UploadPageLocators
import shutil
import browsercmd.common.utils as utils
import json
from random import randint
from selenium.webdriver.common.action_chains import ActionChains
import time,random
import sys
import os
import traceback
class Youtube():
    profile_tmp_download="tmp"
    email=""
    ip_email = "http://178.128.211.227"
    def __init__(self,driver, path_video, title, description, tag,
                 custom_thumb,url_cb_log, job_id, language='en',category='CREATOR_VIDEO_CATEGORY_MUSIC', location="USA"):
        self.driver = driver
        self.retries_upload = 3
        self.path_video= path_video
        self.title = str(title)[:98]
        self.description = str(description)[:4900]
        arr_tag = tag.split(",")
        arr_rs_tag = []
        len_tag = 0
        for tag in arr_tag:
            len_tag += len(tag) + 2
            if len_tag < 490:
                arr_rs_tag.append(tag)
            else:
                break
        self.tag = ",".join(arr_rs_tag)
        self.custom_thumb=custom_thumb
        self.url_cb_log=url_cb_log
        self.language=language
        self.category=category
        self.location=location
        self.job_id=job_id

    def upload(self):
        self.driver.get("https://www.youtube.com/upload?approve_browser_access=1")
        time.sleep(3)
        upload_page= youtube.UploadPage(self.driver)
        if upload_page.is_upload_page():
            if not upload_page.is_avail_upload():
                if(self.retries_upload>0):
                    self.retries_upload = self.retries_upload-1
                    return self.upload()
                else:
                    print("Don't have upload page")
                    utils.call_error(self.url_cb_log, self.job_id, self.email, "5;;Don't have upload page")
                    return
            #for x in range(0,randint(0,3)):
            #    upload_page.click_random_position()
            # time.sleep(1)
            # upload_page.check_language()
            # time.sleep(1)
            print('find upload path')
            upload_page.upload_path_element = self.path_video
            upload_page.wait_upload_done()
            video_link = upload_page.video_link
            print("videoLink: " + video_link)
            upload_page.wait_title_input_avail()
            upload_page.title = self.title
            time.sleep(2)
            # upload_page.click_des()
            # time.sleep(1)
            upload_page.description = self.description
            time.sleep(1)
            upload_page.description = self.description
            time.sleep(2)
            upload_page.click_kids_no()
            time.sleep(1)
            upload_page.click_more_options()
            time.sleep(1)
            upload_page.tag = self.tag
            time.sleep(2)
            if self.custom_thumb != "None" and upload_page.is_custom_thumb():
                upload_page.thumb = self.custom_thumb
            upload_page.set_video_language(self.language)
            upload_page.set_video_category(self.category)
            upload_page.set_video_location(self.location)
            upload_page.click_next()
            upload_page.click_next()
            upload_page.click_public_radio()
            upload_page.click_publish()
            upload_page.click_close()
            time.sleep(1)
            video_link= video_link.replace('https://www.youtube.com/watch?v=','youtube.be/')
            print("Done upload............. :" + video_link)
            utils.call_success(self.url_cb_log, self.job_id, self.email, video_link)
        else:
            print("Don't have upload page")
            utils.call_error(self.url_cb_log, self.job_id,self.email, "5;;Don't have upload page")

    def close(self):
        utils.save_cookie(self.ip_email,self.cookie_cur_folder,self.email)
        self.driver.close()
        self.driver.quit()
        shutil.rmtree(self.cookie_load_folder)
        try:
            os.remove(self.path_video)
            os.remove(self.custom_thumb)
        except:
            pass
    def finish(self):
        utils.unlock_process(self.url_cb_log, self.job_id)
        cmd = "vncserver -kill :77"
        os.popen(cmd).read()
