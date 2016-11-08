import urllib
import bs4
import re
import sys


def get_imgs(url):
    response = urllib.urlopen(url=url)
    detail_html = response.read()
    soap = bs4.BeautifulSoup(detail_html)
    return [img.attrs.get('src') for img in
            soap.select('ul#J_UlThumb li a img')]


if __name__ == '__main__':
    url = sys.argv[1]
    img_src = get_imgs(url)

    for idx, src in enumerate(img_src):
        img_url = 'http:' + re.sub(r'\_\d+x\d+q\d+\.jpg$', "", src)
        img_data = urllib.urlopen(url=img_url).read()
        f = file('../imgs/'+str(idx)+'.jpg', 'wb')
        f.write(img_data)
        f.close()
