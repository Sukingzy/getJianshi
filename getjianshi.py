# coding=utf-8

__author__ = 'WenryXu'

import requests
import bs4
import MySQLdb

# 数据库
db = MySQLdb.connect(host='localhost',
                     user='root',        # 数据库用户名
                     passwd='password',  # 数据库密码
                     db='jianshi',       # 数据库库名
                     charset='utf8',
                     use_unicode=True)
cursor = db.cursor()

baseUrl = 'http://www.jianshu.com'

# 今日看点
response = requests.get('http://www.jianshu.com/')
soup = bs4.BeautifulSoup(response.content, "html.parser")
links = [baseUrl + a.attrs.get('href') for a in soup.select('li div h4.title a')]
titles = [a.text for a in soup.select('li div h4.title a')]

# 获取摘要
for i in range(len(links)):
    response = requests.get(links[i])
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    content = (' '.join(p.text for p in soup.select('div.show-content p'))).strip().lstrip().rstrip(',')[:120] + '...'
    # test
    # print links[i] + ", " + titles[i] + ", " + content
    # print "========== " + str(i) + " =========="
    count = cursor.execute("select * from jianshi where url = '" + links[i] + "'" )
    if count == 0:
        sql = "insert ignore into jianshi(url, title, content, CreateDate) values ('" + links[i] + "', '" + titles[i] + "', '" + content + "', curdate())"
        cursor.execute(sql)

db.close()
