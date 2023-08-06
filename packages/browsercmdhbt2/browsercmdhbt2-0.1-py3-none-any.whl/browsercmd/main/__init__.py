from selenium import webdriver
from browsercmd.common.config import *
from browsercmd.common.utils import *
import shutil
def setup_driver(ipmail,email):
    driver=None
    cookie_cur_folder=None
    try:
        cookie_tmp_folder = os.path.join(get_dir("cookies"),email)
        load_cookie("http://"+ipmail,cookie_tmp_folder, email)
        profile = webdriver.FirefoxProfile(cookie_tmp_folder)
        driver = webdriver.Firefox(firefox_profile=profile, firefox_binary= Selenium.FIREFOX_BIN,
                                        executable_path= Selenium.GEKO_EXECUTE_PATH)
        cookie_cur_folder = driver.capabilities.get('moz:profile')
        shutil.rmtree(cookie_tmp_folder)
    except Exception as e:
        raise e
        pass
    return driver, cookie_cur_folder