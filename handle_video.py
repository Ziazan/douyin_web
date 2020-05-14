'''
@Author: your name
@Date: 2020-05-14 21:49:13
@LastEditTime: 2020-05-14 22:26:22
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /python/douyin_web/handle_video.py
'''
# 接口字段说明见 douyin_web/doc/url_info.md
import re
import requests
import json
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome  import ChromeDriverManager
import ip_list 
import handle_db

class HandleVideoList():
    def __init__(self):
        option = ChromeOptions()
        #移除Selenium中window.navigator.webdriver的值
        option.add_experimental_option('excludeSwitches', ["enable-automation"])
        self.browser = webdriver.Chrome(executable_path = ChromeDriverManager().install(),options=option)

        self.max_cursor = 0 #记录下一次请求的集合数
       
    
    def start(self,url):
        video_list_url = self.get_signature(url)
        try_num = 1 #重试数
        if True:
            #请求视频列表
            json_dict = json.loads(self.handle_request(video_list_url).text)
            if len(json_dict["aweme_list"]) > 0:
                aweme_list = self.handle_video_data(json_dict)
                #存储到db
                self.save_aweme_list(aweme_list)
                #请求下一个
                self.max_cursor = json_dict["max_cursor"] #记录下一次请求需要用到的max_cursor
            elif try_num:
                video_list_url = self.get_signature(url)
                try_num -= 0
            max_cursor_s = re.compile(r'max_cursor=(.*?)&')
            next_list_url = max_cursor_s.sub('_signature=' + str(self.max_cursor)  + '&',video_list_url)
            video_list_url = next_list_url
            print('当前url请求的url',video_list_url)
            time.sleep(3)
    # 处理数据请求
    def handle_request(self,url,header = None):
        requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
        s = requests.session()
        s.keep_alive = False # 关闭多余连接
        #proxies 无用
        proxies = { 
            "http":'http://' + ip_list.get_http_ip(),
            "https": 'https://' +ip_list.get_https_ip()
        }
        print('访问url:',url)
        if(not header):
            header = {
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
            }
        response = requests.get(url=url,headers=header)
        return response

    # js拼接出接口url
    def get_signature(self,url):
        header = {
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
        }
        response = requests.get(url= url,headers=header)
        # sec_uid
        sec_uid = re.search(r"sec_uid=(.*?)&{1}",response.url).group(1)
        print("sec_uid:",sec_uid)

        # dytk
        dytk = re.search(r"dytk:.*?'(.*?)'",response.text).group(1).replace(' ','')
        print("dytk:",dytk)
        
        #signature
        tac_search = re.compile(r"<script>tac=(.*?)</script>")
        uid_search = re.compile(r'uid: "(.*?)",')

        uid = re.search(uid_search,response.text).group(1)
        tac_script ="var tac =" + re.search(tac_search,response.text).group(1) + ";"
        
        # 拼接html
        with open("./file/header_html.txt",'r') as f_header:
            c_header = f_header.read()

        with open("./file/foot_html.txt",'r') as f_footer:
            c_footer = f_footer.read()

        with open("./file/signature.html",'w') as f_signature:
            content = c_header
            content += tac_script + '\n'
            c_footer = c_footer.replace("{{uid}}",uid)
            c_footer = c_footer.replace("{{sec_uid}}",sec_uid)
            c_footer = c_footer.replace("{{max_cursor}}",str(self.max_cursor))
            c_footer = c_footer.replace("{{dytk}}",dytk)
            content += c_footer
            f_signature.write(content)
            f_header.close()
            f_footer.close()
            f_signature.close()

        #请求接口数据
        return self.get_video_list_url()

    #处理视频数据
    def handle_video_data(self,json_data):
        aweme_list = []
        for aweme in json_data["aweme_list"]:
            video_info = {} 
            video_info["author"] = {}
            video_info["author"]["uid"] = aweme["author"]["uid"]
            video_info["author"]["unique_id"] = aweme["author"]["unique_id"] #有时候没有
            video_info["author"]["short_id"] = aweme["author"]["short_id"]
            video_info["author"]["sec_uid"] = aweme["author"]["sec_uid"]

            video_info["aweme_id"] = aweme["aweme_id"]
            video_info["statistics"] = aweme["statistics"] #播放数/评论数/转发数/点赞数 在这里面
            video_info["v_id"] = aweme["video"]["vid"]
            video_info["desc"] = aweme["desc"]
            video_info["play_addr"] = aweme["video"]["play_addr_lowbr"] #无水印。无推荐结尾的url
            video_info["download_addr"] = aweme["video"]["download_addr"] #有水印。有搜索结尾视频
            aweme_list.append(video_info)
            print(video_info,end='\n\n')

        return aweme_list

    #获取视频列表接口的url
    def get_video_list_url(self):
        self.browser.get("file:///Users/ziazan/Documents/project/python/douyin_web/file/signature.html")
        try:
            link = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a'))
            )
            video_list_url = link.text
            _signature_s = re.compile(r'_signature=(.*?)&')
            _signature = re.search(_signature_s,video_list_url).group(1)
            #selemium 生成的signature 和真实的signature 倒数第二位相差1
            code = _signature[-2:-1]
            if not code.isdigit():
                code = chr(ord(code) + 1)
            else:
                code = int(code) + 1

            print('selenium',_signature)
            _signature = _signature[:len(_signature) - 2] + str(code) + _signature[-1]
            print('after',_signature)
            video_list_url = _signature_s.sub('_signature=' + _signature  + '&',video_list_url)
            print('url',video_list_url)
        
        finally:
            self.browser.quit()
        
        return video_list_url
        
    #视频数据保存到数据库
    def save_aweme_list(self,data):
        for item in data:
            handle_db.update_video_info(item)

if __name__ == '__main__':
    url = "https://v.douyin.com/KhkbCq/"#成都消防
    handle_video_list = HandleVideoList()
    handle_video_list.start(url) #获取视频列表
    