import urllib
import bs4
import re
import sys
import os


def get_imgs(detail_html):
    soap = bs4.BeautifulSoup(detail_html)
    return [img.attrs.get('src') for img in
            soap.select('ul#J_UlThumb li a img')]


def get_title(detail_html):
    soap = bs4.BeautifulSoup(detail_html)
    pattern = r'<title>(.*)</title>'
    title = re.findall(pattern, str(soap.select('title')[0]).decode('utf-8'))[0]
    return title


if __name__ == '__main__':
    while (True):
        print 'welcome, please pass the URL and press ENTER!'
        url = sys.stdin.readline()

        response = urllib.urlopen(url=url)
        detail_html = response.read()
        img_src = get_imgs(detail_html)
        folder_name = '../imgs/%s' % get_title(detail_html)
        os.mkdir(folder_name)
        for idx, src in enumerate(img_src):
            print 'downloading now , please wait.'
            img_url = 'http:' + re.sub(r'\_\d+x\d+q\d+\.jpg$', "", src)
            img_data = urllib.urlopen(url=img_url).read()
            f = file('%s/%s.jpg' % (folder_name, str(idx)), 'wb')
            f.write(img_data)
            f.close()
        print 'download images complete!'
