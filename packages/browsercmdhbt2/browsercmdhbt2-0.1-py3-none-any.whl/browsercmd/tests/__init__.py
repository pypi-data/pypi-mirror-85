import unittest
from selenium import webdriver
import browsercmd.common.utils as utils
from browsercmd.main.google import Google
from browsercmd.main.youtube import Youtube
import tempfile
class TestLoadBrowser(unittest.TestCase):
    def setUp(self):
        self.email="estrela.de.gelo.com@gmail.com"
        self.ip_email="http://178.128.211.227"
        tmp=tempfile.gettempdir()
        self.cookie_load_folder =  tmp+"/cookies/" + self.email
        print(self.cookie_load_folder)
        utils.load_cookie(self.ip_email, self.cookie_load_folder, self.email)
        profile = webdriver.FirefoxProfile(self.cookie_load_folder)
        #profile.set_preference("general.useragent.override", self.user_agent)
        self.firefox_binary="F:/Developer/git/python/browsercmd/FirefoxSetup52/core/firefox.exe"
        self.executable_path="F:/Developer/git/python/browsercmd/geckodriver_52.exe"
        self.driver =  webdriver.Firefox(firefox_profile=profile, firefox_binary = self.firefox_binary,
                                      executable_path = self.executable_path)
        self.cookie_cur_folder = self.driver.capabilities.get('moz:profile')
        pass
    def tearDown(self):
        utils.save_cookie(self.ip_email, self.cookie_cur_folder, self.email)
        self.driver.close()
        pass
    def ntest_open_browser(self):
        self.driver.get("http://youtube.com")
        self.assertTrue("youtube" in self.driver.current_url)
    def ntest_login(self):
        google= Google(self.driver, self.email,"1LP11edW25Z01446&*)##","estrela.650656l3y9@gmail.com")
        self.assertTrue(google.login())
    def test_upload(self):
        youtube = Youtube(self.driver,"F:\\Developer\\git\\python\\browsercmd\\final-vid-c51c3c45-0b67-428e-b55b-bb5d3207bf29.avi"
                         ,"this is title","this is description","tag1,tag2,","F:\\Developer\\git\\python\\browsercmd\\wall-416060.jpg")
        youtube.upload()

class TestStringMethods(unittest.TestCase):
    """Sample test case"""

    # Setting up for the test
    def setUp(self):
        pass

    # Cleaning up after the test
    def tearDown(self):
        pass

    # Returns True if the string contains 6 a.
    def test_strings_a(self):
        self.assertEqual('a' * 6, 'aaaaaa')

        # Returns True if the string is in upper case.

    def test_upper(self):
        self.assertEqual('love'.upper(), 'LOVE')

        # Returns True if the string is in uppercase

    # else returns False.
    def test_isupper(self):
        self.assertTrue('LOVE2'.isupper())
        self.assertFalse('Love'.isupper())


if __name__ == '__main__':
    unittest.main()