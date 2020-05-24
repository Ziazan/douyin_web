'''
@Author: your name
@Date: 2020-05-14 21:49:13
@LastEditTime: 2020-05-24 23:54:10
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /python/douyin_web/handle_video.py
'''
# 接口字段说明见 douyin_web/doc/url_info.md
import re
import requests
import json
import time
import asyncio
from pyppeteer import launch

import ip_list 
import handle_db

class HandleVideoList():
    def __init__(self):
        self.browser = None
        self.max_cursor = 0 #记录下一次请求的集合数
       
    
    async def start(self,url):
        video_list_url = await self.get_signature(url)
        print('获取到的url',video_list_url)
        #请求视频列表
        json_dict = json.loads(self.handle_request(video_list_url).text)
        print('json_dict',json_dict)
        if len(json_dict["aweme_list"]) > 0:
            aweme_list = self.handle_video_data(json_dict)
            #存储到db
            self.save_aweme_list(aweme_list)
            #请求下一个
            self.max_cursor = json_dict["max_cursor"] #记录下一次请求需要用到的max_cursor
            
        max_cursor_s = re.compile(r'max_cursor=(.*?)&')
        next_list_url = max_cursor_s.sub('_signature=' + str(self.max_cursor)  + '&',video_list_url)
        video_list_url = next_list_url
        
    # 处理数据请求
    def handle_request(self,url,header = None):
        # requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
        # s = requests.session()
        # s.keep_alive = False # 关闭多余连接
        
        # 代理服务器
        proxyHost = "http-dyn.abuyun.com"
        proxyPort = "9020"

        # 代理隧道验证信息
        proxyUser = "HY8J827KP036E2MD"
        proxyPass = "9709C1E88E2586C4"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host" : proxyHost,
            "port" : proxyPort,
            "user" : proxyUser,
            "pass" : proxyPass,
        }

        proxies = {
            "http"  : proxyMeta,
            "https" : proxyMeta,
        }
        if(not header):
            header = {
                "User-Agent":"Mozilla/5.0 (Linux; Android 7.1.2; SM-G955N Build/N2G48H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36",
            }
        print('proxies',proxies)
        # response = requests.get(url=url,headers=header,proxies=proxies)
        response = requests.get(url=url,headers=header)
        return response

    # js拼接出接口url
    async def get_signature(self,url):
        header = {
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
        }
        response = self.handle_request(url= url,header=header)

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

        #生成js
        with open("./file/page_tmp.js",'r') as f_temp_js:
            c_temp_js = f_temp_js.read()
            c_temp_js = tac_script + '\n' + c_temp_js
            c_temp_js = c_temp_js.replace("{{uid}}",uid)
            c_temp_js = c_temp_js.replace("{{sec_uid}}",sec_uid)
            c_temp_js = c_temp_js.replace("{{max_cursor}}",str(self.max_cursor))
            c_temp_js = c_temp_js.replace("{{dytk}}",dytk)
            with open("./file/page.js",'w') as f_js:
                f_js.write(c_temp_js)
                f_temp_js.close()
                f_js.close()
                
        time.sleep(3)
        #请求接口数据
        return await self.get_video_list_url()

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
    async def get_video_list_url(self):
        if not self.browser:
            self.browser = await launch({
                # 'headless': False, # 关闭无头模式
                # 'devtools': True, # 打开 chromium 的 devtools
                'executablePath':'/Users/ziazan/Documents/soft/chrome-mac/Chromium.app/Contents/MacOS/Chromium',
                'args':[ 
                    '--disable-extensions',
                    '--hide-scrollbars',
                    '--disable-bundled-ppapi-flash',
                    '--mute-audio',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-gpu',
                ],
                # 'dumpio': True,
                },
            )

        page = await self.browser.newPage()
    
        # 设置页面视图大小
        await page.setViewport(viewport={'width':1280, 'height':800})
        
        # 是否启用JS，enabled设为False，则无渲染效果
        await page.setJavaScriptEnabled(enabled=True)
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                            '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299')
        
        #TODO 这里要替换为自己的文件路径
        await page.goto('file:///Users/ziazan/Documents/project/python/douyin_web/file/signature.html')
               
        # 加入设置webdriver为false的代码
        await page.evaluate("""
            () =>{
                Object.defineProperties(navigator,{
                    webdriver:{
                    get: () => false
                    }
                })
            }
        """)
        
        await page.addScriptTag(path='./file/page.js')
        print('page',page.content)

        # 抓取链接
        link_elements = await page.xpath('/html/body/a')
        for item in link_elements:
            # 获取链接
            video_list_url = await (await item.getProperty('textContent')).jsonValue()
        
        print('video_list_url',video_list_url)
        # video_list_url = link.text
        _signature_s = re.compile(r'_signature=(.*?)&')
        _signature = re.search(_signature_s,video_list_url).group(1)

        # 打印页面文本
        # print(await page.content())
        #selemium 生成的signature 和真实的signature 倒数第二位相差1
        # code = _signature[-2:-1]
        # if not code.isdigit():
        #     code = chr(ord(code) + 1)
        # else:
        #     code = int(code) + 1

        print('bdefore',_signature)
        # _signature = _signature[:len(_signature) - 2] + str(code) + _signature[-1]
        print('after',_signature)
        video_list_url = _signature_s.sub('_signature=' + _signature  + '&',video_list_url)
        print('url',video_list_url)
        
        print("_signature",_signature)
        return video_list_url
        
    #视频数据保存到数据库
    def save_aweme_list(self,data):
        for item in data:
            handle_db.update_video_info(item)

async def main():
    url = "https://v.douyin.com/KhkbCq/"#成都消防
    # url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=MS4wLjABAAAAaJO9L9M0scJ_njvXncvoFQj3ilCKW1qQkNGyDc2_5CQ&count=35&max_cursor=0&aid=1128&_signature=mnEVIRARxNjphx9OFJJc75pxFT&dytk=5b2632429035ae972ca049e9414387e6"
    handle_video_list = HandleVideoList()
    await handle_video_list.start(url) #获取视频列表
    # response = handle_video_list.handle_request(url)
    # print('response',response.text)

if __name__ == '__main__':
   loop = asyncio.get_event_loop()
   loop.run_until_complete(main())
    