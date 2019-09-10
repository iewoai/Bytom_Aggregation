#coding=utf-8
import jieba, re
import pymysql 
import os
import sys
import redis
from urllib import parse
from gensim import corpora,models,similarities

#url解码
a_id = re.escape(sys.argv[1])

#查询所有文本数据
db = pymysql.connect("localhost","root","fang","bytom")
cursor = db.cursor()
sql1 = "set names utf8"
sql = "select id,content,title from content_text"

cursor.execute(sql1)
cursor.execute(sql)
res = cursor.fetchall()
id_list = []
text_list = []
test = []
for data in res:
	#得到分词矩阵
    if(data[0]!=int(a_id)):
    	id_list.append(data[0])
    	text_list.append(data[1].split(" "))
    else:
    	test = data[1].split(" ")
    	


#制作词库
dictionary = corpora.Dictionary(text_list)
corpus = [dictionary.doc2bow(doc) for doc in text_list]
#测试集
test = dictionary.doc2bow(test)    

#训练模型
tfidf = models.TfidfModel(corpus)

index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))
sim = index[tfidf[test]]
#获取相似度结果
res = sorted(enumerate(sim), key=lambda item: -item[1])

res = res[:5]

#存储推荐结果到redis
res_list = []
for i in res:
	res_list.append(id_list[i[0]])
print(res_list)
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)  
r = redis.Redis(connection_pool=pool)
r.hset("recommend",a_id,str(res_list))


   
