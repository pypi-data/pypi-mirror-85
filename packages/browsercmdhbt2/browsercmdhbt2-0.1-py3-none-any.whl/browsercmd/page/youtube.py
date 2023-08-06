from . import BasePage

from browsercmd.elements.youtube import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time, random
from browsercmd.common.config import ImageResource
from random import randint
import pyautogui


class UploadPage(BasePage):
    upload_path_element = UploadElement()
    title = TitleUploadElement()
    description = DescriptionUploadElement()
    tag = TagUploadElement()
    thumb = ThumbnailUploadElement()
    video_link = VideoLinkUploadElement()

    def check_language(self):
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element(*UploadPageLocators.LANGUAGE_BUTTON))
        if "English" in self.driver.find_element(*UploadPageLocators.LANGUAGE_BUTTON).text:
            print("Ok English")
        else:
            print("change language")
            self.driver.find_element(*UploadPageLocators.LANGUAGE_BUTTON).click()
            time.sleep(1)
            self.driver.find_element(*UploadPageLocators.LANGUAGE_ENGLISH_US).click()
            time.sleep(3)

    def is_custom_thumb(self):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(UploadPageLocators.CUSTOM_THUMB_BUTTON))
            return True
        except Exception as e:
            print(e)
        return False

    def set_video_language(self,lang_code):
        try:
            form_select = self.driver.find_element(*UploadPageLocators.LANG_FORM_SELECT)
            self.driver.execute_script("arguments[0].scrollIntoView();", form_select)
            time.sleep(1)
            form_select.click()
            time.sleep(1)
            LANG_SUB_ITEM = (By.XPATH, f'//paper-item[@test-id="{lang_code}"]')
            lang_item = self.driver.find_element(*LANG_SUB_ITEM)
            self.driver.execute_script("arguments[0].scrollIntoView();", lang_item)
            time.sleep(1)
            lang_item.click()
            time.sleep(1)
            return True
        except Exception as e:
            print(e)
        return False

    def set_video_category(self,cate_code):
        try:
            form_select = self.driver.find_element(*UploadPageLocators.CATEGORY_FORM_SELECT)
            self.driver.execute_script("arguments[0].scrollIntoView();", form_select)
            time.sleep(1)
            form_select.click()
            time.sleep(1)
            CATEGORY_SUB_ITEM = (By.XPATH, f'//paper-item[contains(@test-id,"{cate_code}")]')
            cate_item = self.driver.find_element(*CATEGORY_SUB_ITEM)
            self.driver.execute_script("arguments[0].scrollIntoView();", cate_item)
            time.sleep(1)
            cate_item.click()
            time.sleep(1)
            return True
        except Exception as e:
            print(e)
        return False

    def set_video_location(self,location_code):
        try:
            vidloc_input = self.driver.find_element(*UploadPageLocators.VIDEO_LOCATION_INPUT)
            vidloc_input.clear()
            vidloc_input.send_keys(location_code)
            time.sleep(1)
            VIDEO_LOCATION_SUB_ITEM = (
            By.XPATH, f'//paper-item[contains(@test-id,"title")]')
            item = self.driver.find_element(*VIDEO_LOCATION_SUB_ITEM)
            self.driver.execute_script("arguments[0].scrollIntoView();", item)
            time.sleep(1)
            item.click()
            time.sleep(1)
            return True
        except Exception as e:
            print(e)
        return False

    def wait_custom_thumb_avail(self):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(UploadPageLocators.THUMB_AVAIL))
            return True;
        except Exception as e:
            print(e)
        return False;

    def wait_upload_done(self):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(UploadPageLocators.PROGRESS_BAR))
            value_now = 0
            while int(value_now) < 100:
                progress_bar_e = self.driver.find_element(*UploadPageLocators.PROGRESS_BAR)
                value_now = progress_bar_e.get_attribute("aria-valuenow")
                print(f"Upload: {value_now} %")
                time.sleep(5)
        except Exception as e:
            print(e)
            pass

    def wait_title_input_avail(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(UploadPageLocators.TITLE))
            return True;
        except Exception as e:
            print(e)
        return False;

    def is_upload_page(self):
        print("check is_upload_page: " + self.driver.current_url)
        return "/videos/upload" in self.driver.current_url

    def is_avail_upload(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(UploadPageLocators.START_BUTTON_UPLOAD))
            self.driver.find_element(*UploadPageLocators.START_BUTTON_UPLOAD)
            return True
        except Exception as e:
            print(e)
        return False

    def click_des(self):
        try:
            self.driver.find_element(By.XPATH,"//ytcp-mention-textbox[contains(@class,\"description-textarea\")]").click()
        except:
            pass
        return True
    def click_kids_no(self):
        try:
            self.driver.find_element(*UploadPageLocators.KIDS_NOT_MADE_BUTTON).click()
        except:
            pass
        return True

    def click_more_options(self):
        try:
            self.driver.find_element(*UploadPageLocators.MORE_OPTIONS_BUTTON).click()
        except:
            pass
        return True

    def click_next(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(UploadPageLocators.NEXT_BUTTON))
            self.driver.find_element(*UploadPageLocators.NEXT_BUTTON).click()
        except Exception as e:
            print(e)
            pass
        return True

    def click_public_radio(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(UploadPageLocators.PUBLIC_RADIO))
            self.driver.find_element(*UploadPageLocators.PUBLIC_RADIO).click()
        except Exception as e:
            print(e)
            pass
        return True

    def click_publish(self):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(UploadPageLocators.PUBLISH_BUTTON))
            self.driver.find_element(*UploadPageLocators.PUBLISH_BUTTON).click()
        except  Exception as e:
            print(e)
            pass
        return True

    def click_close(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(UploadPageLocators.CLOSE_BUTTON))
            self.driver.find_element(*UploadPageLocators.CLOSE_BUTTON).click()
        except Exception as e:
            print(e)
            pass
        return True

    def click_random_position(self):
        buttons = {0: ImageResource.ICON_PUBLIC, 1: ImageResource.UPLOAD_BUTTON}
        res = buttons.get(randint(0, 1))
        time_click = randint(1, 3)
        print(res)
        buttonx, buttony = pyautogui.locateCenterOnScreen(res)
        pyautogui.leftClick(buttonx, buttony, time_click)

    def publish_no_crash(self):
        try:
            WebDriverWait(self.driver, 1000).until(
                lambda driver: 'Click' in driver.find_element(*UploadPageLocators.NOTIFY).text)
        except:
            pass
        try:
            time.sleep(random.randrange(20) + 5)
            WebDriverWait(self.driver, 1000).until(
                EC.element_to_be_clickable(UploadPageLocators.PUBLISH))
            self.driver.find_element(*UploadPageLocators.PUBLISH).click()
        except:
            pass

    def is_cannot_upload_strike(self):
        try:
            self.driver.find_element(*UploadPageLocators.FAIL_UPLOAD_STRIKE)  # check Strike
            return True
        except:
            pass
        return False

    def publish(self):
        # publish check crash
        count = 0
        while count < 1000:
            try:
                if 'Click' in self.driver.find_element(*UploadPageLocators.NOTIFY).text:
                    break
            except:
                pass
            try:
                self.driver.find_element(*UploadPageLocators.RESTORE_BUTTON)  # check crash
                return False
            except:
                pass
            try:
                self.driver.find_element(*UploadPageLocators.FAIL_UPLOAD_STRIKE)  # check Strike
                return False
            except:
                pass
            count += 1
            time.sleep(1)
        try:
            time.sleep(random.randrange(20) + 5)
            WebDriverWait(self.driver, 1000).until(
                EC.element_to_be_clickable(UploadPageLocators.PUBLISH))
            self.driver.find_element(*UploadPageLocators.PUBLISH).click()
        except:
            pass
        return True


class WatchPage(BasePage):
    def subscribe(self):
        try:
            self.driver.find_element(*WatchPageLocators.SUBS_BUTTON).click()
        except:
            pass


class EditPage(BasePage):
    def publish(self):
        try:
            video_id = self.driver.find_element(*EditPageLocators.PUBLISH_BUTTON).get_attribute("data-video-id")
            self.driver.get("https://www.youtube.com/edit?o=U&video_id=" + video_id)
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.find_element(
                    *UploadPageLocators.TITLE))
            if "hbt2" not in self.driver.find_element(*UploadPageLocators.TITLE).text:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: driver.find_element(
                        *EditPageLocators.SAVE_BUTTON))
                self.driver.find_element(*EditPageLocators.SAVE_BUTTON).click()
                time.sleep(5)
        except:
            pass
