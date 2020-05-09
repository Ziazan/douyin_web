'''
@Author: your name
@Date: 2020-05-09 16:54:20
@LastEditTime: 2020-05-09 23:56:05
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /python/douyin_web/video_download.py
'''
import video_list_url
import handle_db
import time

#下载视频
def download_video(uid):
    userInfo = handle_db.get_video_url(uid)
    header = {
         "User-Agent":"Mozilla/5.0 (Linux; Android 7.1.2; SM-G955N Build/N2G48H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36",
        }
    print('正在下载:【%s】的视频....\n'%userInfo['nick_name'])
    for item in userInfo['video_list']:
        url = item['play_addr']['url_list'][1]
        response = video_list_url.handle_request(url = url,header = header)
        with open('video/%s.mp4'%item['aweme_id'],'wb') as data_file:
            data_file.write(response.content)
        time.sleep(2)
        
if __name__ == "__main__":
    uid = '110812020268'
    download_video(uid)
