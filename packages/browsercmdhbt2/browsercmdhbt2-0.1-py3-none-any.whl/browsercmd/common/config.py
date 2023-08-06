import os
class ServerAdress(object):
    IP="http://167.99.74.94"
class Selenium(object):
    FIREFOX_BIN="F:/Developer/git/python/browsercmd/FirefoxSetup52/core/firefox.exe"
    GEKO_EXECUTE_PATH="F:/Developer/git/python/browsercmd/geckodriver_52.exe"
class ImageResource(object):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    ICON_GOOGLE=dir_path+"/res/google.png"
    ICON_PUBLIC=dir_path+"/res/public.png"
    UPLOAD_BUTTON=dir_path+"/res/upload_button.png"
    RECOVERY_MAIL=dir_path+"/res/confirm_email.png"



