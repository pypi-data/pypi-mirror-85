from selenium.webdriver.common.by import By

class UploadPageLocators(object):
    INPUT= (By.XPATH,'//input[@type="file"]')
    TITLE= (By.XPATH,'//ytcp-mention-textbox[contains(@class,\"title-textarea\")]//div[@id="textbox"]')
    DESCRIPTION=(By.XPATH,'//ytcp-mention-textbox[contains(@class,\"description-textarea\")]//div[@id="textbox"]')
    TAG=(By.XPATH,'//input[@id="text-input" and @aria-label="Tags"]')
    NOTIFY=(By.XPATH,'//div[contains(@class,"upload-item-alert")]/div[@class="yt-alert-content"]/div[@class="yt-alert-message"]')
    IS_ON_PUBLISH=(By.XPATH,'//div[@class="save-cancel-buttons"]/button[contains(.,"Publish") and not(@disabled)]')
    PUBLISH=(By.XPATH,'//div[@class="save-cancel-buttons"]/button[contains(.,"Publish")]')
    LANGUAGE_BUTTON=(By.ID,'yt-picker-language-button')
    LANGUAGE_ENGLISH_US=(By.XPATH,"//button[contains(.,\"English\")]")
    CUSTOM_THUMB_BUTTON = (By.XPATH, "//ytcp-thumbnails-compact-editor-uploader//button")
    CUSTOM_THUMB=(By.XPATH,"//ytcp-thumbnails-compact-editor-uploader//input")
    THUMB_AVAIL=(By.XPATH,'//div[contains(@class,"custom-thumb")]//img')
    VIDEO_LINK=(By.XPATH,'//span[contains(@class,"video-url-fadeable")]/a[contains(@class,"ytcp-video-info")]')
    START_BUTTON_UPLOAD=(By.XPATH,'//ytcp-button[@id="select-files-button"]')
    RESTORE_BUTTON=(By.XPATH,'//button[@id="restoreTab"]')
    FAIL_UPLOAD_STRIKE=(By.XPATH,'//div[@id="active-uploads-containbutton"]//div[contains(.,"cannot upload")]')
    KIDS_NOT_MADE_BUTTON = (By.XPATH, '//paper-radio-button[@name="NOT_MADE_FOR_KIDS"]')
    KIDS_MADE_BUTTON = (By.XPATH, '//paper-radio-button[@name="MADE_FOR_KIDS"]')
    VIDEO_LOCATION_INPUT = (By.XPATH, '//input[@aria-label="Video location"]')
    VIDEO_LOCATION_SUB_ITEM=(By.XPATH,'//paper-item[contains(@test-id,"title") and contains(@test-id,"Vietnam")]')
    NEXT_BUTTON=(By.XPATH,'//ytcp-button[@id="next-button"]')
    PUBLISH_BUTTON=(By.XPATH,'//ytcp-button[@id="done-button"]')
    PUBLIC_RADIO = (By.XPATH,'//paper-radio-button[@name="PUBLIC"]')
    CLOSE_BUTTON = (By.XPATH, '//ytcp-button[@id="close-button"]')
    MORE_OPTIONS_BUTTON=(By.XPATH,'//ytcp-button[contains(@class,"ytcp-uploads-details")]')
    LANG_FORM_SELECT = (By.XPATH, '//ytcp-form-select[contains(@class,"ytcp-form-language-input")]')
    CATEGORY_FORM_SELECT = (By.XPATH, '//ytcp-form-select[@id="category"]')
    VIDEO_LOCATION_INPUT = (By.XPATH, '//input[@aria-label="Video location"]')
    PROGRESS_BAR = (By.XPATH,
                       '//ytcp-video-upload-progress/paper-progress[@role="progressbar" and contains(@class,"ytcp-video-upload-progress")]')

class WatchPageLocators(object):
    SUBS_BUTTON = (By.XPATH,"//div[@id=\"subscribe-button\"]//yt-formatted-string[text()=\"Subscribe\"]")

class EditPageLocators(object):
    PUBLISH_BUTTON = (By.XPATH, "//button[contains(@class,\"vm-video-publish\") and @data-video-id]")
    SAVE_BUTTON = (By.XPATH, "//button[contains(@class,\"save-changes-button\")]")
