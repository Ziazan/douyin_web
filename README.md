<!--
 * @Author: your name
 * @Date: 2020-05-03 18:04:10
 * @LastEditTime: 2020-05-10 00:49:34
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: /python/douyin_web/README.md
 -->

# 通过抖音的分享页抓取视频信息

## 目标
通过抖音用户主页的分享链接例如：[https://v.douyin.com/KhkbCq/](https://v.douyin.com/KhkbCq/)
获取用户的基本信息，如：粉丝数/视频数/视频评论量/视频发布时间/视频点赞数

## 思路记录
 访问分享链接之后，获取用户的基本信息。抖音id/昵称/点赞数/关注数/粉丝数
 分析视频列表接口的规则，生成视频列表访问的url,此url中的signature 需要生成一个html文件，`selenium`打开html文件能获取。（见 [signature分析.md](https://github.com/Ziazan/douyin_web/blob/master/doc/signature%E5%88%86%E6%9E%90.md)文件）

 在视频列表接口返回的json中 可以拿到 视频的基本信息和视频播放地址
 再用`requests`访问视频下载地址,下载视频到本地。
 此项目使用mongodb 存储数据

## 项目文件说明：
1. 读需要爬取的抖音用户的分享页链接写在`share_task.txt`中
2. 运行 `handle_share.py` 获取`share_task.txt`配置的抖音用户的基本信息 点赞数/关注数/粉丝数
3. 运行 `video_list_url.py`获取用户的视频列表信息： 点赞数/关注数/转发数/评论数
4. 运行`video_download.py`下载指定用户的所有无水印视频保存到`video`文件夹


## 运行截图
![https://github.com/Ziazan/douyin_web/blob/master/doc/img/user_info.png](https://github.com/Ziazan/douyin_web/blob/master/doc/img/user_info.png)

![https://github.com/Ziazan/douyin_web/blob/master/doc/img/download_video.png](https://github.com/Ziazan/douyin_web/blob/master/doc/img/download_video.png)

![https://github.com/Ziazan/douyin_web/blob/master/doc/img/video_lsit.png](https://github.com/Ziazan/douyin_web/blob/master/doc/img/video_lsit.png)


## 视频链接获取的 signature 分析
见 [signature分析.md](https://github.com/Ziazan/douyin_web/blob/master/doc/signature%E5%88%86%E6%9E%90.md)文件

## 遇到的报错
Q:Message: 'chromedriver' executable needs to be in PATH. Please see https://sites.google.com/a/chromium.org/chromedriver/home

A:
使用 ChromeDriverManager 去下载对应chrome版本的 ChromeDriver
```
pip install webdriver-manager
```
```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

```

参考：[https://stackoverflow.com/questions/29858752/error-message-chromedriver-executable-needs-to-be-available-in-the-path](https://stackoverflow.com/questions/29858752/error-message-chromedriver-executable-needs-to-be-available-in-the-path)

Q: `signature.html` 总是不能正确拿到视频列表的接口url 
![https://github.com/Ziazan/douyin_web/blob/master/doc/img/error1.png](https://github.com/Ziazan/douyin_web/blob/master/doc/img/error1.png)

A：使用selenium 和正常打开的浏览器生成的sigenature不一样。 有可能是 在js代码中判别了浏览器的原因。
[如何突破网站对selenium的屏蔽](https://blog.csdn.net/clf63082/article/details/100223126?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-2&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-2)

方法一：想到js中删除相关关键词，但是js代码都混淆加密过了。**不可行**

方法二：把selenium浏览器伪装成真实浏览器

[如何正确移除Selenium中window.navigator.webdriver的值](https://cloud.tencent.com/developer/article/1397806)

```python
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = Chrome(options=option)
```
使用这个方法，生成的signature
selenium 中生成的结果：
Q94FRRAeHXEwKA8qaryWr0PeAV

正常浏览器的结果：
Q94FRRAeHXEwKA8qaryWr0PeBV

目前只剩倒数第二位的数值是相差1的结果。
见`video_list_url.py` 中`get_video_list_url()`方法

Q:urllib3.exceptions.MaxRetryError: HTTPConnectionPool(host='127.0.0.1', port=62785): Max retries exceeded with url: /session/8a9ff6e4be66e9833b0a16750c5fe67e/url (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x110acd7c0>: Failed to establish a new connection: [Errno 61] Connection refused'))
A:....好像ip被封了。要找代理了

Q:request 配置代理的时候报错：urllib3.exceptions.ProxySchemeUnknown: Not supported proxy scheme None
A：
```python
 proxies = { 
        "http":'http://' + ip_list.get_http_ip(),
        "https": 'https://' +ip_list.get_https_ip()}
```
格式需要是 http:// + ip + :端口

## 参考
1. [xpath helper 插件](https://blog.csdn.net/love666666shen/article/details/72613143)
2. [在线字体编辑器](https://kekee000.github.io/fonteditor/)
3. [Python爬虫如何获取重定向后的url](https://blog.csdn.net/lclfeng/article/details/88647616)
4. [2020抖音无水印视频解析真实地址](https://blog.csdn.net/qq_36737934/article/details/104127835)
5. [Python selenium 模拟Chrome浏览器打开手机模式](https://www.cnblogs.com/yiwenrong/p/12664414.html)