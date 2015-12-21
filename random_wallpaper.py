#!/usr/bin/env python
#coding=utf-8

__author__ = 'reelai'
__mtime__ = '15/10/8'

import time
import logging
import shutil
import  datetime
import random
import re
import os
import subprocess
import requests
from bs4 import BeautifulSoup

def exec_cmd(cmdline,output='stdout'):
    logging.info('doing:%s'%cmdline)
    try:
        p=subprocess.Popen(cmdline,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        stdout,stderr=p.communicate()
        if output in 'stdout':
            result = stdout
        if output in 'stderr':
            result = stderr
    except Exception,e:
        result = None
    return  result



def get_content_from_url(url):
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"}
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text,'html.parser')
    return soup

def random_pagenumber(url):
    soup = get_content_from_url(url)
    page_number = []
    for link in soup.find_all('a',href=re.compile(r'Date/\d{3,}')):
        page_number.append(str(link.text))
    page_number.sort()
    max_page = int(page_number[-1])
    return random.randint(1,max_page)


def random_imgurl(choose_url):
    soup = get_content_from_url(choose_url)
    imgurl_list = []
    for link in soup.find_all('a'):
        l = link.find('img')
        if l:
            url = link['href']
            if  url.startswith(u'/mac'):
                imgurl_list.append(link['href'])
    return str(imgurl_list[random.randrange(0,len(imgurl_list)-1)])


def check_retina_15(imgurl):
    soup = get_content_from_url(imgurl)
    for link in soup.find_all('a',text=u'Retina MacBook Pro 15-inch (2880x1800)'):
        return link['href']


def download_img(imgurl):
    logging.info('downloading:%s'%imgurl)
    local_path = os.path.join(today_path,imgurl.split('/')[-1])
    # local_path = os.path.join(SAVE_PATH,file_name)
    r = requests.get(imgurl,stream=True)
    if r.status_code ==200:
        with open(local_path,'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw,f)
    logging.info('download complete..save to:%s',local_path)
    return local_path


def set_wallpaper(imgpath):
    script  = """/usr/bin/osascript<<EOF
                tell application "Finder"
                set desktop picture to POSIX file "%s"
                end tell
                EOF"""
    # subprocess.Popen(script%imgpath,shell=True)
    cmd = script%imgpath
    exec_cmd(cmd)



def del_old(rootpath,keep_max):
    d ={}
    l = []
    drop_list = []
    cmdline = 'find %s -type d'%rootpath
    dirlist = exec_cmd(cmdline)
    for d in dirlist.split():
        if re.findall(r'\d{4}-\d{2}-\d{2}',d):
            l.append(d)
    if len(l) > KEEP_MAX:
        drop_list.extend(sorted(l)[0:len(l)-KEEP_MAX])

    for d in drop_list:
        exec_cmd("rm -rf %s"%d)



if __name__ == '__main__':

    WEBSITE='http://www.allmacwallpaper.com'
    BASEURL = WEBSITE + '/retina-macbook-pro-wallpapers/Date'

    SAVE_PATH ='/Users/reelai/Pictures/allmacwallpaper.com'
    KEEP_MAX=7

    logging.basicConfig(filename=__file__.split('.')[0]+'.log',level=logging.INFO,filemode='a',format='%(asctime)s - %(levelname)s: %(message)s')
    logging.info('-----------starting-%s------------'%datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    today = datetime.datetime.now().strftime('%Y-%m-%d')
    today_path = os.path.join(SAVE_PATH,today)

    if not os.path.exists(today_path):
        os.makedirs(today_path)


    imgurl_retina_15 = None
    while not imgurl_retina_15:
        random_url = BASEURL+'/'+str(random_pagenumber(BASEURL))  #1-502随机选择
        choose_imgurl= WEBSITE+random_imgurl(random_url)  #随机选择一个图
        imgurl_retina_15 = check_retina_15(choose_imgurl)

    imgurl_retina_15 = WEBSITE + imgurl_retina_15
    file_path= download_img(imgurl_retina_15)
    set_wallpaper(file_path)
    del_old(SAVE_PATH,KEEP_MAX)
