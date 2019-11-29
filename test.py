import urllib.request
import os
import re
import http
from bs4 import BeautifulSoup

def download(url, user_agent='wswp', num_retries=2):
    print('Downloading:', url)
    # headers = {'User-agent': user_agent}
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

url = 'https://mp.weixin.qq.com/s/LOiwF3pyfEiK-ZvZXWOtRg'
html = download(url)

urllist = re.findall("url: '(.*?),", html)
print(test)