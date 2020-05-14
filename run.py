'''
@Author: your name
@Date: 2020-05-14 21:06:11
@LastEditTime: 2020-05-14 22:23:07
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /python/douyin_web/run.py
'''
import time
import handle_share
import handle_video
import handle_db

#开始
def start():
    _ = input('请确保你已经在./share_task.text 中保存用户主页的分享链接:（Y/N）\n')
    if _ == 'y' or _ == 'Y' :
        handle_share.init_task_info() #处理任务基本信息
        user_list = handle_db.get_user_list() #展示数据
        handle_video_list = handle_video.HandleVideoList()
        for user_info in user_list:
            handle_video_list.start(user_info['share_link']) #获取视频列表
            handle_db.show_data_list(user_info['uid'])#展示用户信息
            time.sleep(3)
            # handle_db.download_file() #下载视频
        
        

if __name__ == '__main__':
    # 输入抖音分享主页
    # 显示用户的信息
    # 下载视频
    start()
    pass