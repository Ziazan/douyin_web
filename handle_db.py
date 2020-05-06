'''
@Author: your name
@Date: 2020-05-01 22:54:45
@LastEditTime: 2020-05-07 00:28:42
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /python/douguo/handle_mongo.py
'''
import pymongo

from pymongo.collection import Collection
import requests


client = pymongo.MongoClient(host="127.0.0.1",port=27017)
db = client['douyin']

#初始化任务
def handle_init_task():
    task_id_collection = Collection(db,'task_id')
    with open('./file/share_task.txt','r') as f_task:
        for task_info in f_task.readlines():
            task = {}
            task['share_link'] = task_info.replace('\n','')
            task_id_collection.insert(task)


#获取任务信息
def handle_get_task():
    task_id_collection = Collection(db,'task_id')
    return task_id_collection.find_one_and_delete({})

#插入用户信息
def inser_user(item):
    user_info_collection = Collection(db,'user_info')
    user_info_collection.insert(item)

def update_video_info(item):
    user_info_collection = Collection(db,'user_info')
    query = {"uid":item['author']['uid']}
    # user_dict = item['author'].items() + query.items()
    user_dict = dict(item['author'], **query)
    new_info = { "$set": user_dict}
    user_info_collection.update_one(query,new_info)

    del item["author"]
    video_value = { "$addToSet": {"video_list":{"$each":[item]}}}
    user_info_collection.update_one(query,video_value)

def get_video_url(uid):
    user_info_collection = Collection(db,'user_info')
    data = user_info_collection.find({'uid':uid})
    return data[0]
    
def download_file(url, path):
    with requests.get(url, stream=True) as r:
        chunk_size = 1024
        content_size = int(r.headers['content-length'])
        print('下载开始')
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)

#展示数据
def show_data_list():
    print("视频下载url:",end="\n\n")
    uid = '110812020268'
    data = get_video_url(uid)
    print("名称:%s"%data['nick_name'],end='\n')
    print("ID:%s"%data['uid'],end='\n')
    print("个性签名:%s"%data['signature'][0],end='\n')
    print("粉丝数:%s"%data['follows'],end='\n')
    print("关注数:%s"%data['focus'],end='\n')
    print("获赞数:%s"%data['liked_num'],end='\n')
    print("视频数量:%s"%len(data['video_list']),end='\n')
    print("==========视频列表============\n")
    for item in data['video_list']:
         print("视频描述:%s"%item['desc'],end='\n')
         print("点赞数：%s  评论数：%s  转发数：%s"%(item['statistics']['digg_count'],item['statistics']['comment_count'],item['statistics']['share_count']),end='\n')
         print("**需要打开浏览器的手机调试模式**\n:")
         print("视频播放地址:%s"%item['download_addr']['url_list'][0],end='\n')
         print("无水印下载地址:%s"%item['download_addr']['url_list'][1],end='\n\n')


if __name__ == "__main__":
    show_data_list()
    #TODO  还需要使用selenium 打开视频页面，去获取到下载地址
    # handle_init_task()
    # download_file('https://aweme.snssdk.com/aweme/v1/play/?video_id=v0200fa00000bplloe3rh3penp00qcag&line=0&ratio=540p&watermark=1&media_type=4&vr_type=0&improve_bitrate=0&logo_name=aweme&is_support_h265=0&source=PackSourceEnum_PUBLISH','./video/test.mp4')
    pass