#coding=utf-8

import jieba, re
import jieba.analyse

import pymysql
import traceback

from lib import nlp
from lib import store_data
from spider import jianshu,zhifu,bit,csdn


if __name__=='__main__':
    #文本数据存储的类
    dis = store_data.store_data()
    #文本处理类
    nlp = nlp.nlp()
    
    
    #处理每一个item
    def deal_item(c_plat,platform,type):
        obj = eval(platform+"."+platform+"()")
        if type=="get_data":
            items = obj.get_data()
        else:
            items = obj.get_newest_data()
        for item in items:
            print("开始处理"+item['title']) 
            print(item['url'])
            #存储单个item数据
            #特殊字符转义 
            item['text'] = item['title']*2+item['text']
            item['info'] = re.escape(item['info'])
            item['title'] = re.escape(item['title'])
            item['author'] = re.escape(item['author'])
            
            id = dis.store_data(item,c_plat)
            dis.store_hot(c_plat,item['hot'])
            cut = nlp.get_cut(item['text'])
            
            dis.store_text(cut,id,item['title'])
            #self.store_tag(item['tag'])
            print("处理完毕"+"="*20)
            
      
    
    
    #从数据库获取全部的文本信息
    def get_text():
        sql1 = "set names utf8"
        sql = "select id,content from content_text"
        #记录热度基数
        dis.cursor.execute(sql1)
        dis.cursor.execute(sql)
        res = dis.cursor.fetchall()
        
        id_list = []
        text_list = []
        for data in res:
            id_list.append(data[0])
            #每个分词用空格隔开
            text_list.append(data[1])
        #获取关键字
        return id_list,text_list
            
    deal_item("简书","jianshu","get_data")
    deal_item("知乎","zhifu","get_data")
    deal_item("CSDN","csdn","get_data")
    deal_item("巴比特","bit","get_data")
    
    
    #开始利用tf-idf获取关键词
    id_list,text_list = get_text()
    
    print("开始获取关键字")
    key = nlp.get_keywords(text_list)    
    print("获取关键字结束")
    #存储前5标签
    #清空标签数据库
    db = pymysql.connect("localhost","root","fang","bytom" )
    cursor = db.cursor()
    cursor.execute("delete from tag where 1=1")
    db.commit()
    f=0
    for k in key:
        try:
            dis.store_tag_in_content_text(k, id_list[f])
            dis.store_tag_in_article(k[0:5], id_list[f])
            dis.store_tag_in_tag(k[0:5])
            f = f+1
        except:
            f = f+1
            traceback.print_exc()