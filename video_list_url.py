'''
@Author: your name
@Date: 2020-05-05 10:01:21
@LastEditTime: 2020-05-05 10:59:47
@LastEditors: Please set LastEditors
@Description: 获取用户抖音列表的接口url
@FilePath: /python/douyin_web/file/video_list_url.py
'''

# 接口字段说明见 douyin_web/doc/url_info.md
import re
import requests

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

if __name__ == '__main__':
    get_signature()
