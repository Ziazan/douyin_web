'''
@Author: your name
@Date: 2020-05-03 14:01:13
@LastEditTime: 2020-05-06 00:10:32
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /python/douyin_web/handle_share.py
'''

import re
import requests
import handle_db
import time
from lxml import etree

#解析页面数据
def handle_decode(content):
    
    #抖音数据集合
    regex_list = [
        {'name':[' &#xe603; ',' &#xe60d; ',' &#xe616; '],'value':0},
        {'name':[' &#xe602; ',' &#xe60e; ',' &#xe618; '],'value':1},
        {'name':[' &#xe605; ',' &#xe610; ',' &#xe617; '],'value':2},
        {'name':[' &#xe604; ',' &#xe611; ',' &#xe61a; '],'value':3},
        {'name':[' &#xe606; ',' &#xe60c; ',' &#xe619; '],'value':4},
        {'name':[' &#xe607; ',' &#xe60f; ',' &#xe61b; '],'value':5},
        {'name':[' &#xe608; ',' &#xe612; ',' &#xe61f; '],'value':6},
        {'name':[' &#xe60a; ',' &#xe613; ',' &#xe61c; '],'value':7},
        {'name':[' &#xe60b; ',' &#xe614; ',' &#xe61d; '],'value':8},
        {'name':[' &#xe609; ',' &#xe615; ',' &#xe61e; '],'value':9},
    ]

    #替换数字字符
    for regex_num in regex_list:
        for num_code in regex_num['name']:
           pattern = re.compile(r'<i class="icon [^>"]*?">%s</i>' %num_code)
           content = re.sub(pattern,str(regex_num["value"]),content)

    share_web_html = etree.HTML(content)
    user_info = {}

    #昵称
    user_info["nick_name"] = share_web_html.xpath("//p[@class='nickname']/text()")[0]
    #抖音id
    user_info["user_id"] = ''.join(share_web_html.xpath("//p[@class='shortid']/text()")).replace(' ','').replace('抖音ID：','')
    #个性签名
    user_info['signature'] = share_web_html.xpath("//p[@class='signature']/text()")
    #粉丝数
    user_info['follows'] = ''.join(share_web_html.xpath("//p[@class='follow-info']//span[@class='follower block']//span[@class='num']/text()")).replace(' ','')
    #关注数
    user_info['focus'] = ''.join(share_web_html.xpath("//p[@class='follow-info']//span[@class='focus block']//span[@class='num']/text()")).replace(' ','')
    #点赞数
    user_info['liked_num'] = ''.join(share_web_html.xpath("//p[@class='follow-info']//span[@class='liked-num block']//span[@class='num']/text()")).replace(' ','')
    #职业
    user_info['job'] = ''.join(share_web_html.xpath("//div[@class='verify-info']//span[@class='info']/text()")).replace(' ','')
    user_info['video_list'] = []
    print("用户信息：====",end="\n")
    print(user_info)
    handle_db.inser_user(user_info)

#获取抖音用户分享页面的数据
def handle_douyin_share(task):
    url = task['share_link']
    header = {
        "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    }
    response = requests.get(url=url,headers=header)
    #解码信息
    handle_decode(response.text)
   
MAX_COUNT = 3
if __name__ == '__main__': 
    count = MAX_COUNT
    while count :
        task = handle_db.handle_get_task()
        if not task:
            handle_db.handle_init_task()
        else:
            handle_douyin_share(task)
            count -= 1
            time.sleep(1)
        