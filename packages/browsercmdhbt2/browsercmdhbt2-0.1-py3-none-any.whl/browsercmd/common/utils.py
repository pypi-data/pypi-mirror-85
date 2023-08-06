import requests
import os
import datetime
from gbackup import *
import uuid

from .config import ServerAdress
__all__ =["load_cookie","save_cookie","download_file","get_dir"]

def download_gdrive(id,email, path):
    drh = DriverHelper()
    conf = drh.create_driver_config(email)
    Client(conf, "download", path, "").download_file(id,path)
def download_file(url, root_dir=None, ext= None):
    rs = None
    try:
        if ext:
            file_name = str(uuid.uuid4()) + "." + ext
        else:
            file_name = os.path.basename(url)
        if not root_dir:
            rs = os.path.join(get_dir('download'),file_name)
        else:
            rs =os.path.join(root_dir,file_name)
        if "gdrive" in url:
            download_gdrive(url.split(";;")[-1],url.split(";;")[-2],rs)
        else:
            r = requests.get(url)
            with open(rs, 'wb') as f:
                f.write(r.content)
    except:
        rs = None
        pass
    return rs

def get_dir(dir):
    tmp_download_path =os.path.join(tempfile.gettempdir(),dir)
    if not os.path.exists(tmp_download_path):
        os.makedirs(tmp_download_path)
    return tmp_download_path

def make_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
def load_cookie(api_address,cookie_folder,email):
    try:
        make_folder(cookie_folder)
        r = requests.get(api_address+"/automail/api/cookie/get/"+email)
        with open(cookie_folder+"/cookies.sqlite", 'wb') as f:
            f.write(r.content)
    except:
        pass

def save_cookie(api_address,cookie_folder,email):
    with open(cookie_folder+"/cookies.sqlite", 'rb') as f:
        files = {'file':('cookies.sqlite',f)}
        data={'fileName':email}
        requests.post("http://"+api_address+"/automail/api/mail/upload/", data=data,files=files)
def call_success(server_address,job_id,gmail,video_id):
    log_data="s;;"+ str(datetime.datetime.now())+";;"+gmail+";;"+video_id;
    data={'id':job_id,'success':1,'log_data':log_data}
    requests.post(server_address,data=None,json=data)

def unlock_process(server_address,job_id):
    log_data="f;;"+ str(datetime.datetime.now());
    data={'id':job_id,'log_data':log_data}
    requests.post(server_address,data=None,json=data)

def call_error(server_address,job_id,gmail,log):
    log_data="e;;"+ str(datetime.datetime.now())+";;"+gmail+";;"+log;
    data={'id':job_id,'success':0,'log_data':log_data}
    requests.post(server_address,data=None,json=data)
    
def get_video():
    return requests.get("http://news.singerchart.com/msn/link/get").text;


