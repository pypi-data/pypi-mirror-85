from browsercmd.main.google import Google
from browsercmd.main.youtube import Youtube
from browsercmd.main import setup_driver
from browsercmd.common import utils
import requests
import tempfile
import json,zipfile,shutil,os

def upload_youtube(job_id, config):
    gmail=config['gmail']
    ip_email= config['ip_email']
    link_video= config['link_video']
    video_ext=config['video_ext']
    link_thumbnail = config['link_thumbnail']
    title = config['title']
    description = config['description']
    tag = config['tag']
    language = config['language']
    category = config['category']
    location = config['location']
    url_cb_log = config['url_cb_log']
    root_dir = tempfile.TemporaryDirectory()
    try:
        obj = requests.post(f'http://{ip_email}/automail/api/mail/get/',json={"gmail":gmail}).json()
        pass_word=obj['pass_word']
        recovery_email=obj['recovery_email']
        root_dir=tempfile.TemporaryDirectory()
        driver, cookie_folder=setup_driver(ip_email, gmail)
        if driver and cookie_folder:
            google = Google(driver,gmail,pass_word,recovery_email)
            if google.login():
                video_path = utils.download_file(link_video,root_dir.name, ext=video_ext)
                thumb_path = utils.download_file(link_thumbnail,root_dir.name, ext='jpg')
                if video_path:
                    youtube = Youtube(driver,video_path,title,description,tag,thumb_path,url_cb_log, job_id, language, category,location)
                    youtube.upload()
    except:
        pass
    close(ip_email, gmail, driver, cookie_folder)
    root_dir.cleanup()

def close(ip_email, email, driver, cookie_folder):
    try:
        if driver:
            utils.save_cookie(ip_email, cookie_folder, email)
            driver.close()
            driver.quit()
    except:
        pass
    try:
        if cookie_folder:
            shutil.rmtree(cookie_folder)
            #os.popen("rm -rf "+ cookie_folder).read()
    except:
        pass


def upload_youtube_by_drive_config(job_id, config):
    gmail = config['gmail']
    ip_email = config['ip_email']
    language = config['language']
    category = config['category']
    location = config['location']
    url_cb_log = config['url_cb_log']
    drive_config_link = config['drive_config_link']
    root_dir = tempfile.TemporaryDirectory()
    try:
        zip_path = utils.download_file(drive_config_link, root_dir.name, ext="zip")
        zip_folder=os.path.join(root_dir.name,"zip_tmp")
        with zipfile.ZipFile(zip_path,"r") as zip_ref:
            zip_ref.extractall(zip_folder)
        with open(os.path.join(zip_folder,'config.txt')) as json_file:
            obj_config = json.load(json_file)
            title = obj_config['title']
            description = obj_config['description']
            tag = obj_config['tag']
            video_path = os.path.join(zip_folder,obj_config['video_path'])
            thumb_path = os.path.join(zip_folder,obj_config['thumb_path'])
        if title:
            obj = requests.post(f'http://{ip_email}/automail/api/mail/get/', json={"gmail": gmail}).json()
            pass_word = obj['pass_word']
            recovery_email = obj['recovery_email']
            driver, cookie_folder = setup_driver(ip_email, gmail)
            if driver and cookie_folder:
                google = Google(driver, gmail, pass_word, recovery_email)
                if google.login():
                    if video_path:
                        youtube = Youtube(driver, video_path, title, description, tag, thumb_path,url_cb_log,job_id, language, category,
                                          location)
                        youtube.upload()
    except:
        pass
    close(ip_email, gmail, driver, cookie_folder)
    root_dir.cleanup()

