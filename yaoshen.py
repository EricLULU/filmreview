import requests
from bs4 import BeautifulSoup
from urllib import parse
import time
import random

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Cookie':'ll="118163"; bid=6poLcloprc0; ps=y; __yadk_uid=eB3xk0Mi3PC3X4quM2Kqswqqd5j8xlkf; douban-profile-remind=1; push_noty_num=0; push_doumail_num=0; ap=1; ue="2589325627@qq.com"; _ga=GA1.2.213364547.1534073016; gr_user_id=29717bc5-de47-4d1d-9e10-5e4d3829cce8; douban-fav-remind=1; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1534555494%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; ap_v=1,6.0; _vwo_uuid_v2=DF379698041E5187DA88AA31D8B80302E|992fb1b807a9f9f6aa09546de6071038; _pk_id.100001.4cf6=e6074ae87c69a30a.1534073763.2.1534556048.1534074512.; _pk_ses.100001.4cf6=*; __utma=30149280.213364547.1534073016.1534476831.1534555492.5; __utmb=30149280.4.10.1534555492; __utmc=30149280; __utmz=30149280.1534476831.4.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.16455; __utma=223695111.213364547.1534073016.1534073763.1534555494.2; __utmb=223695111.0.10.1534555494; __utmc=223695111; __utmz=223695111.1534555494.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
    'Host':'movie.douban.com',
    'Referer':'https://movie.douban.com/subject/26752088/comments?sort=time&status=P',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
}

session = requests.Session()
session.headers.update(headers)

file = open('yaoshen.txt','a',encoding='utf-8')

def url_create():
    start_url = "https://movie.douban.com/subject/26752088/comments?"
    for page in range(11):

        params = {
            'start':page*20,   #这个是控制当前页的
            'limit':20,    #每页限制的数量
            'sort':'new_score',
            'status':'P',
            }
        url = start_url + parse.urlencode(params)
        yield url

def html_get(url, num_retries=2):
    global session
    try:
        time.sleep(random.random()*5)
        html = session.get(url).content
    except:
        if num_retries > 0:
            html_get(url, num_retries-1)
        else:
            print("下载失败：",url)
    else:
        return html

def info_get(html):
    info_item = {}  #存储字典
    soup = BeautifulSoup(html, 'lxml')
    comments = soup.find(id='comments')
    for comment in comments.find_all(class_="comment-item"):
        print(len(comments))
        #print(comment)
        ava_a = comment.find(class_="avatar").find('a') 
        info_item = {
                'nickname':ava_a.attrs['title'],
                'link': ava_a.attrs['href'],
                'img_link': ava_a.find('img').attrs['src'],
            }
        com = comment.find(class_="comment")
        #print(com)
        info_item['votes'] = com.find(class_="comment-vote").find(class_="votes").string
        info_item['content'] = com.find('p').find('span').string.replace('\n','')

        yield info_item  #将提取的信息返回

def info_show(item):
    global file
    print("短评内容是:",item['content'])
    file.write(item['content'] + ' ')

def main():
    """
        调度程序
    """
    for url in url_create():
        html = html_get(url)
        #对结果进行判断
        if html == None:
            print('html出错:', html)
        else:
            item_list = info_get(html)
            for item in item_list:
                info_show(item)

if __name__ == '__main__':
    try:
        main()
    finally:
        file.close()   #关闭文件

