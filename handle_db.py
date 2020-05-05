'''
@Author: your name
@Date: 2020-05-01 22:54:45
@LastEditTime: 2020-05-05 10:57:36
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

# handle_init_task()
print(handle_get_task())

