'''
@Author: your name
@Date: 2020-05-05 09:46:13
@LastEditTime: 2020-05-05 09:47:56
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /python/douyin_web/redirect.py
'''

import requests
 
 
def get_redirect_url():
    # 重定向前的链接
    url = "https://v.douyin.com/KhkbCq/"
    # 请求头，这里我设置了浏览器代理
    header = {
        "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    }
    # 请求网页
    response = requests.get(url, headers=header)
    print(response.status_code)  # 打印响应的状态码
    print(response.url)  # 打印重定向后的网址
    # 返回重定向后的网址
    return response.url
 
 
if __name__ == '__main__':
    get_redirect_url()
