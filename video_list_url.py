'''
@Author: your name
@Date: 2020-05-05 10:01:21
@LastEditTime: 2020-05-05 19:31:00
@LastEditors: Please set LastEditors
@Description: 获取用户抖音列表的接口url
@FilePath: /python/douyin_web/file/video_list_url.py
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
from webdriver_manager.chrome import ChromeDriverManager


# 处理数据请求
def handle_request(url):
    header = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
    }

    response = requests.get(url=url,headers=header)
    return response

# js拼接出接口url
def get_signature():
    url = "https://v.douyin.com/KhkbCq/"
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
        c_footer = c_footer.replace("{{dytk}}",dytk)
        content += c_footer
        f_signature.write(content)
        f_header.close()
        f_footer.close()
        f_signature.close()

    handle_video_list_url()

#处理视频数据
def handle_video_data(json_data):
    aweme_list = []
    for aweme in json_data['aweme_list']:
        video_info = {} 
        video_info["aweme_id"] = aweme['aweme_id']
        video_info["statistics"] = aweme['statistics'] #播放数/评论数/转发数/点赞数 在这里面
        video_info["v_id"] = aweme['video']['vid']
        video_info["desc"] = aweme['desc']
        video_info['play_addr'] = aweme['video']['play_addr_lowbr'] #无水印。无推荐结尾的url
        video_info['download_addr'] = aweme['video']['download_addr'] #有水印。有搜索结尾视频
        aweme_list.append(video_info)
        

    return aweme_list

#获取视频列表接口的url
def handle_video_list_url():
    browser.get("file:///Users/ziazan/Documents/project/python/douyin_web/file/signature.html")
    try:
        link = WebDriverWait(browser, 10).until(
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

        print('before',_signature)
        _signature = _signature[:len(_signature) - 2] + code + _signature[-1]
        print('after',_signature)
        video_list_url = _signature_s.sub('_signature=' + _signature  + '&',video_list_url)
        print('url',video_list_url)

        #请求视频列表
        json_dict = json.loads(handle_request(video_list_url).text)
    finally:
        browser.quit()
    max_cursor = json_dict['max_cursor'] #记录下一次请求需要用到的max_cursor
    aweme_list = handle_video_data(json_dict)
    print(aweme_list)
    print(max_cursor)

if __name__ == '__main__':
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    browser = webdriver.Chrome(executable_path = ChromeDriverManager().install(),options=option)
    get_signature()


