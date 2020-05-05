'''
@Author: your name
@Date: 2020-05-01 22:54:45
@LastEditTime: 2020-05-06 00:18:32
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /python/douguo/handle_mongo.py
'''
import pymongo

from pymongo.collection import Collection


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
    query = {"user_id":item['author']['unique_id']}
    # user_dict = item['author'].items() + query.items()
    user_dict = dict(item['author'], **query)
    new_info = { "$set": user_dict}
    user_info_collection.update_one(query,new_info)

    del item["author"]
    video_value = { "$addToSet": {"video_list":{"$each":[item]}}}
    user_info_collection.update_one(query,video_value)

if __name__ == "__main__":
    # handle_init_task()
    print(handle_get_task())

