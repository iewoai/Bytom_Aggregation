#coding=utf-8
import jieba, re
import pymysql 
import os
import sys
import redis
from urllib import parse

def get_cut(content):
    path = os.path.dirname(os.path.abspath(__file__))
    content = re.sub(r'\s|\n', '', content)
    jieba.initialize()
    jieba.load_userdict(path+"/dict.txt")
    jieba.add_word("比原链")
    jieba.add_word("区块链")
    jieba.add_word("以太坊")
    res = jieba.cut_for_search(content)
    stop_words = get_stop_words()
    
    words_list = []
    for i in res:
        if i not in stop_words:
            words_list.append(i)
    return words_list
    
def get_stop_words():
    path = os.path.dirname(os.path.abspath(__file__))
    stopwords = []
    for word in open(path+"/STOPWORDS.txt", "r",encoding="utf-8"):
        stopwords.append(word.strip())

    return stopwords    


#url解码
keywords = get_cut(parse.unquote(sys.argv[1]))

sessionId = sys.argv[2]
#查询数据
db = pymysql.connect("localhost","root","fang","bytom" )
cursor = db.cursor()
sql1 = "set names utf8"
sql = "select id,content,title from content_text"

cursor.execute(sql1)
cursor.execute(sql)
res = cursor.fetchall()
id_dict = {}
for data in res:
    id_dict[str(data[0])]=0
    for key in keywords:
        
        id_dict[str(data[0])] =id_dict[str(data[0])]+len(re.findall(key,data[1],flags=re.IGNORECASE))
    for key in keywords:
        #赋予标题的权值为5
        id_dict[str(data[0])] =id_dict[str(data[0])]+len(re.findall(key,data[2],flags=re.IGNORECASE)*1000)

id_list=[]

key_words = sorted(id_dict.items(),key=lambda x:x[1],reverse=True)   
for i in key_words:
    if i[1]!=0:
        id_list.append(int(i[0]))



#把查询结果存入redis数据库 
# host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)  
r = redis.Redis(connection_pool=pool)
r.set(sessionId, str(id_list))


   
