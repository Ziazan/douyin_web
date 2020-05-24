'''
@Author: your name
@Date: 2020-05-24 19:35:00
@LastEditTime: 2020-05-24 22:30:01
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /python/douyin_web/pyppeter.py
'''
import asyncio
from pyppeteer import launch

async def main():
    # headless参数设为False，则变成有头模式
    browser = await launch({
       'executablePath':'/Users/ziazan/Documents/soft/chrome-mac/Chromium.app/Contents/MacOS/Chromium'
        }
    )
    
    page = await browser.newPage()
    
    # 设置页面视图大小
    await page.setViewport(viewport={'width':1280, 'height':800})
    
    # 是否启用JS，enabled设为False，则无渲染效果
    await page.setJavaScriptEnabled(enabled=True)
    
    await page.goto('https://www.toutiao.com/')
    
    # 打印页面cookies
    print(await page.cookies())
    
    # 打印页面文本
    print(await page.content())
    
    # 打印当前页标题
    print(await page.title())
    
    # 抓取新闻标题
    title_elements = await page.xpath('//div[@class="title-box"]/a')
    for item in title_elements:
        # 获取文本
        title_str = await (await item.getProperty('textContent')).jsonValue()
        print(await item.getProperty('textContent'))
        # 获取链接
        title_link = await (await item.getProperty('href')).jsonValue()
        print(title_str)
        print(title_link)
    
    # 关闭浏览器
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())