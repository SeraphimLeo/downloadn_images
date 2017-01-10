import urllib
import bs4
import re
import sys
import os
import platform
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def get_focus_imgs(detail_html):
    soap = bs4.BeautifulSoup(detail_html)
    return [img.attrs.get('src') for img in
            soap.select('ul#J_UlThumb li a img')]


def get_detail_imgs(detail_html):
    soap = bs4.BeautifulSoup(detail_html)
    # return [img.attrs.get('src') for img in soap.select(
    #     'div#description div.content img.img-ks-lazyload')]

    for img in soap.select('div#description div.content img.img-ks-lazyload'):
        if img.attrs.get('alt') is not None:
            yield img.attrs.get('src')


def get_title(detail_html):
    soap = bs4.BeautifulSoup(detail_html)
    pattern = r'<title>(.*)</title>'
    title = re.findall(pattern, str(soap.select('title')[0]).decode('utf-8'))[0]

    return re.sub(r'([(^\.)\/\.:<>])', '', title)


def load_page(url):
    print u'loading page, please wait.'
    driver = webdriver.PhantomJS()
    driver.get(url)
    # detail = driver.find_element_by_id('description')
    WebDriverWait(driver, 5000).until(
        EC.presence_of_element_located((By.ID, "description"))
    )

    h = 500
    while (True):
        driver.execute_script('window.scrollTo(0,%d)' % h)
        h = h + 500
        time.sleep(1)
        currentHeight = driver.execute_script(
            'return document.body.scrollHeight')
        print u'scroll\t', h, '\total\t', currentHeight
        if currentHeight <= h:
            print u'analysis page, please wait...'
            break
    page_source = driver.page_source.encode('utf-8')

    return page_source


if __name__ == '__main__':

    systemName = platform.system()
    phantomjs = ''

    while (True):
        print 'welcome, please pass the URL and press ENTER!'
        url = sys.stdin.readline()

        detail_html = load_page(url)
        focus_img_src = get_focus_imgs(detail_html)
        detail_img_src = get_detail_imgs(detail_html)

        folder_name = '../imgs/%s' % get_title(detail_html)
        if os.path.exists(folder_name) is False:
            os.mkdir(folder_name)

        for idx, src in enumerate(focus_img_src):
            print 'downloading focus images, please wait.'

            focus_img_folder = folder_name + '/focus'
            if os.path.exists(focus_img_folder) is False:
                print u'create the focus image folder'
                os.mkdir(focus_img_folder)

            img_url = 'http:' + re.sub(r'\_\d+x\d+q\d+\.jpg$', "", src)
            img_data = urllib.urlopen(url=img_url).read()
            f = file('%s/%s.jpg' % (focus_img_folder, str(idx)), 'wb')
            f.write(img_data)
            f.close()

        for idx, src in enumerate(detail_img_src):
            print 'download detail images, please wait.'

            detail_img_folder = folder_name + '/detail'
            if os.path.exists(detail_img_folder) is False:
                print u'create the detail image folder'
                os.mkdir(detail_img_folder)

            img_data = urllib.urlopen(url=src).read()
            f = file('%s/%s.jpg' % (detail_img_folder, str(idx)), 'wb')
            f.write(img_data)
            f.close()

        print 'download images complete!'
        print ''
