import urllib.request
import os
import re
import http
from bs4 import BeautifulSoup


def getContentsInTag(tag, soup):
    contents = []
    
    for content in soup.find_all(tag):
        contents.append(content.get_text(strip=True))
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

def write2File(filename, titel, context):
    
    if os.path.isfile(filename):
        return
    else:
        with open(filename, 'w', encoding='utf-8') as fid:
            fid.write(titel)
            for content in context:
                fid.write(content+'\n')


if __name__ == '__main__':
    # urllist = ['https://mp.weixin.qq.com/s?__biz=MzAwMDEwMDQ1NA==&mid=2651375935&idx=1&sn=114e333c2703a55e5da2ad58233f90e0&chksm=81127836b665f120675b0ecb3f629f8ae43cffcb16c4b368d73b77379d571ae240f0f164dc87&mpshare=1&scene=1&srcid=&sharer_sharetime=1574396750654&sharer_shareid=ed58f180990676c5aadaf17d030f87c0&key=6f374bbe4cd766cf005c6c07f86b05f0e8d6b7358de741592d31ae552d19fd2bd602155bf431404bde978b3e0169bc1bf37d92012cbb1177e54c8e29237fdceabd9a4f5929e64b86aefcfe5bb21ae889&ascene=1&uin=MjIwNzY2NTU4Mg%3D%3D&devicetype=Windows+10&version=62070158&lang=zh_CN&pass_ticket=mIQADLBHUyaZotZpvykQDA%2FPr%2BN9OSs85wrYdc1zESVtiL5XCxVduXQ9Vt7dUV%2BV',
    #            'https://mp.weixin.qq.com/s?__biz=MjM5NTAxOTk1Ng==&mid=2650808148&idx=2&sn=6a381602f5f50e96ea7fee47a28652de&chksm=bd0a528f8a7ddb991e0e59da7cee3c35fc65a095e0e6a1c81bc6c89f44cf6d880b555a70f063&mpshare=1&scene=1&srcid=1119YgKBYlZBUqdLhNtuaQVE&sharer_sharetime=1574170323758&sharer_shareid=ed58f180990676c5aadaf17d030f87c0&key=e737c3fbf5b542744641af2f158023bbe48b201b110b0e4369c0f1b593d1156f5c724b1045bbb002565aac96a8a59294df19945b8079991e0ad9a08ebf81347d24b6cd687b9e48191fae51f06bda405b&ascene=1&uin=MjIwNzY2NTU4Mg%3D%3D&devicetype=Windows+10&version=62070158&lang=zh_CN&pass_ticket=mIQADLBHUyaZotZpvykQDA%2FPr%2BN9OSs85wrYdc1zESVtiL5XCxVduXQ9Vt7dUV%2BV',
    #            'https://mp.weixin.qq.com/s?__biz=MzIyNTQzNDY0NA==&mid=2247489087&idx=2&sn=198f05720432bb8cd7c93ccc655736b0&chksm=e87e9b44df0912527c3dac00290509942ba90c1347fc8c5dccc13c8b9b6144fef269c295f574&mpshare=1&scene=1&srcid=&sharer_sharetime=1573026720611&sharer_shareid=ed58f180990676c5aadaf17d030f87c0&key=e737c3fbf5b5427476ec92f92b4ec5454f6130d86f44620e897126a8820089704f0e55136b02fd017ca3c79ad324d0569241ab25094780c64db566fb560886915653ee491872e2522321257472b85b6d&ascene=1&uin=MjIwNzY2NTU4Mg%3D%3D&devicetype=Windows+10&version=62070158&lang=zh_CN&pass_ticket=mIQADLBHUyaZotZpvykQDA%2FPr%2BN9OSs85wrYdc1zESVtiL5XCxVduXQ9Vt7dUV%2BV',
    #            'https://mp.weixin.qq.com/s?__biz=MzA4MDA0MzcwMA==&mid=2652532912&idx=2&sn=562e1c06e84c173975228afac230039c&chksm=84449b6bb333127dfc24d3491cf5d96dd11eb7148103ba58a3011676b1db2fc61761b47e6921&mpshare=1&scene=1&srcid=&sharer_sharetime=1572900873159&sharer_shareid=ed58f180990676c5aadaf17d030f87c0&key=6f374bbe4cd766cf19113aec8181baf5e7ac3eedda3dcfa0284b165fa21a1570bc331202d5722fdce61b8acbc1c2a8bc0947ce129af2c2001c58d850e8706ebb6f59d3b5a0fd26122edaf890be9aba5b&ascene=1&uin=MjIwNzY2NTU4Mg%3D%3D&devicetype=Windows+10&version=62070158&lang=zh_CN&pass_ticket=mIQADLBHUyaZotZpvykQDA%2FPr%2BN9OSs85wrYdc1zESVtiL5XCxVduXQ9Vt7dUV%2BV',
    #            'https://mp.weixin.qq.com/s?__biz=MjM5MDA2MzMyMA==&mid=2651966224&idx=1&sn=019b0e1bd88de27058bc37c1be965f06&chksm=bdafe4a78ad86db11d164c22404c67e67fab0566279e76f917b0ec24db282bebe63478e61f04&mpshare=1&scene=1&srcid=&sharer_sharetime=1572900714694&sharer_shareid=ed58f180990676c5aadaf17d030f87c0&key=6cd25b8355ad8f57aa998db3c31337f468eb018506831aa4a260f3a7d962294660594316e7e95f66b69c19dc6931d21dda778f4392000594142a258e72212cf7ace9673dbf0e8252d8e6e1e803c3ab22&ascene=1&uin=MjIwNzY2NTU4Mg%3D%3D&devicetype=Windows+10&version=62070158&lang=zh_CN&pass_ticket=mIQADLBHUyaZotZpvykQDA%2FPr%2BN9OSs85wrYdc1zESVtiL5XCxVduXQ9Vt7dUV%2BV',
    #            'https://mp.weixin.qq.com/s?__biz=MzA3MDczNDQwMw==&mid=2652676877&idx=1&sn=6b5baf0a33f48cebc22a82958693294c&chksm=84d04421b3a7cd3717957be37d62ce90792b5227580cac32d688de1c09f9d5630d879d50c224&mpshare=1&scene=1&srcid=&sharer_sharetime=1572888519174&sharer_shareid=ed58f180990676c5aadaf17d030f87c0&key=575ce680ed1368dc2c4ffa619084e3964888406793687fc24bf9173333a00bf8ce8bc055c3834008764f6de28a24f3cbcf747610a43a64ab02c159585b2c6791c6402107edc51383e54ebf7c98daca60&ascene=1&uin=MjIwNzY2NTU4Mg%3D%3D&devicetype=Windows+10&version=62070158&lang=zh_CN&pass_ticket=mIQADLBHUyaZotZpvykQDA%2FPr%2BN9OSs85wrYdc1zESVtiL5XCxVduXQ9Vt7dUV%2BV',
    #            'https://mp.weixin.qq.com/s?__biz=MzA3Mjc5NzUxOQ==&mid=2653210757&idx=2&sn=1543338dea64fed2749a9893450934e2&chksm=84c8b4a5b3bf3db32cd8889a515c0c0543d51609064469b498091c6ae5eec84fc2ebd01f61a8&mpshare=1&scene=1&srcid=&sharer_sharetime=1572895540909&sharer_shareid=ed58f180990676c5aadaf17d030f87c0&key=6f374bbe4cd766cf8a305b7944482dc12fd30a7e6448482b0c4e746454cafbeb23d28f41edc1a37389eb13bef033e8809b95e0913a5718f352e7ecdae00850e6ef9053d9e2f4415fb7f02eb3c8d625d5&ascene=1&uin=MjIwNzY2NTU4Mg%3D%3D&devicetype=Windows+10&version=62070158&lang=zh_CN&pass_ticket=mIQADLBHUyaZotZpvykQDA%2FPr%2BN9OSs85wrYdc1zESVtiL5XCxVduXQ9Vt7dUV%2BV',
    #            'https://mp.weixin.qq.com/s?__biz=MzA3OTEzMjMwNg==&mid=2651910851&idx=1&sn=3bab6172deb60c7caebf4a1abccf0538&chksm=845c713eb32bf8282e4a9c971198d398f06ea940bcf9cd78eb98537ffeb97cf8d8e91221a728&mpshare=1&scene=1&srcid=&sharer_sharetime=1572791743208&sharer_shareid=ed58f180990676c5aadaf17d030f87c0&key=e737c3fbf5b54274138c4e78994e2942e4f836aa2ab2086a64837c7dac342b3c3f11fe89f8d46a616c3e8298def578a060d159bcc3a32f476cb231a91170f38aad0abe7b883a9bb52da4470d7594519e&ascene=1&uin=MjIwNzY2NTU4Mg%3D%3D&devicetype=Windows+10&version=62070158&lang=zh_CN&pass_ticket=mIQADLBHUyaZotZpvykQDA%2FPr%2BN9OSs85wrYdc1zESVtiL5XCxVduXQ9Vt7dUV%2BV'
    #            ]
    # url = 'https://mp.weixin.qq.com/s/LOiwF3pyfEiK-ZvZXWOtRg'
    # html = download(url)

    # urllist = re.findall("url: '(.*?),", html)
    urllist = ['https://mp.weixin.qq.com/s/HrcJS7uHCN14vM4_y51y1w']
    for url in urllist:
        print("Carwler...\n")
        html = download(url)
        soup = BeautifulSoup(html, 'lxml')
        
        titel = getTitel(soup)
        print(titel)
        postfix = 'txt'
        tag = 'p'
        context = getContentsInTag(tag, soup)
        filename = '.'.join([titel.strip().split()[0], postfix])
        if os.path.isfile(filename):
            pass
        else:
            filenamep = '.'.join([titel.strip().split()[0]+'p', postfix])
            filenamespan = '.'.join([titel.strip().split()[0]+'span', postfix])
            write2File(filenamep, titel, context)
            fsizep = os.path.getsize(filenamep)
            tag = 'span'
            context = getContentsInTag(tag, soup)
            write2File(filenamespan, titel, context)
            fsizespan = os.path.getsize(filenamespan)
            if fsizep >= fsizespan:
                os.remove(filenamespan)
                os.rename(filenamep, filename)
            else:
                os.remove(filenamep)
                os.rename(filenamespan, filename)
        print("Finished!")
    

    
   