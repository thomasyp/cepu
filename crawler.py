import urllib.request
from bs4 import BeautifulSoup
import re
import http

def getContentsInTag(tag, soup):
    contents = []
    
    for content in soup.find_all(tag):
        contents.append(content.get_text())
    return contents

def getTitel(soup):
    contents = None
    taglist = ['h1', 'h2', 'h3']
    for tag in taglist:
        for content in soup.find_all(tag):
            contents = content.get_text()
            if contents:
                return contents
    return contents

def download(url, user_agent='wswp', num_retries=2):
    print('Downloading:', url)
    headers = {'User-agent': user_agent}
    response = urllib.request.urlopen(url)
    try:
        html = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(url, user_agent, num_retries-1)
    except http.client.IncompleteRead as e:
        page = e.partial
        html = page.decode('utf-8')
    
    return html

def write2File(filename, titel, context):
    postfix = 'txt'
    filename = '.'.join([titel.strip().split()[0], postfix])
    with open(filename, 'w', encoding='utf-8') as fid:
        fid.write(titel)
        for content in context:
            fid.write(content+'\n')


if __name__ == '__main__':
    html = download('https://mp.weixin.qq.com/s/EFzUrN4qYx2yFz4nXArwpQ')
    soup = BeautifulSoup(html,'lxml')
    tag = 'p'
    context = getContentsInTag(tag, soup)
    titel = getTitel(soup)
    print(titel)
    postfix = 'txt'
    filename = '.'.join([titel.strip().split()[0], postfix])
    write2File(filename, titel, context)
    

    
   