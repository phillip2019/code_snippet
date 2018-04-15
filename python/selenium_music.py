#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Do."""
# @Date    : 2018-01-18 20:03:12
# @Author  : wuyan (msn734506700@live.com)
# @Version : V0.1
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
import time
import urllib

# 歌曲名
mname = '十年'

# JS重定向
def wait(driver):
    elem = driver.find_element_by_tag_name('html')
    count = 0
    while True:
        count += 1
        if count > 20:
            print('chao shi le')
            return
        time.sleep(.5)
        try:
            elem == driver.find_element_by_tag_name('html')
        except StaleElementReferenceException:
            return

#获取url
def geturl():
    input_string = '十年'
    if not input_string:
        input_string = raw_input('>>>please input the search key:')
    driver = webdriver.Chrome('/Users/xiaowei.song/Downloads/chromedriver')
    url = 'http://www.kugou.com/'
    driver.get(url)
    a = driver.find_element_by_xpath('html/body/div[1]/div[1]/div[1]/div[1]/input') #输入搜索内容
    # a.send_keys(input_string.decode('gb18030'))
    a.send_keys(input_string)
    driver.find_element_by_xpath('html/body/div[1]/div[1]/div[1]/div[1]/div/i').click() #点击搜索
    result_url = driver.current_url
    driver.quit()
    return result_url


#显示搜索结果
def show_results(url):
    driver = webdriver.Chrome('/Users/xiaowei.song/Downloads/chromedriver')
    driver.get(url)
    time.sleep(3)
    for i in range(1, 1000):
        try:
            print('%d. ' % i + driver.find_element_by_xpath(".//*[@id='search_song']/div[2]/ul[2]/li[%d]/div[1]/a" % i).get_attribute('title'))  #获取歌曲名
        except NoSuchElementException as msg:
            break
    choice = 1
    # choice = input(">>>Which one do you want(you can input 'quit' to goback(带引号)):")
    if choice == 'quit':   #从下载界面退回
        result = 'quit'
    else:
        global mname
        mname = driver.find_element_by_xpath(".//*[@id='search_song']/div[2]/ul[2]/li[%d]/div[1]/a" % choice).get_attribute('title')
        # a = driver.find_element_by_xpath(".//*[@id='search_song']/div[2]/ul[2]/li[%d]/div[1]/a" % choice)
        a = driver.find_element_by_xpath(".//*[@id='search_song']/div[2]/ul[2]/li[%d]/div[1]/a" % 1)
        actions = ActionChains(driver)
        actions.move_to_element(a)
        actions.click(a)
        actions.perform()
        # wait(driver)
        driver.switch_to_window(driver.window_handles[1])  # 跳转到新打开的页面
        result = driver.find_element_by_xpath(".//*[@id='myAudio']").get_attribute('src') # 获取播放元文件url
        driver.quit()
    return result


#下载回调
def cbk(a, b, c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('%.2f%%' % per)


def main():
    hello = """
        ***********************************************************************
        ***********************欢迎使用GREY音乐下载器*****************************
        **********************directed by GreyyHawk****************************
        ***********************************************************************
    """
    print(hello)
    time.sleep(1)
    while True:
        url = geturl()
        result = show_results(url)
        if result == 'quit':
            print('\n')
            continue
        else:
            local = os.path.join('/Users/xiaowei.song/Downloads', '{}.mp3'.format(mname))
            print('download start')
            time.sleep(1)
            urllib.urlretrieve(result, local, cbk)
            print('finish downloading %s.mp3'%mname + '\n\n')



if __name__ == '__main__':
  main()