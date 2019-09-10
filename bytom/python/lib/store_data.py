#coding=utf-8

import pymysql
import traceback

class store_data:
    def __init__(self):
        self.db = pymysql.connect("localhost","root","fang","bytom" )
        self.cursor = self.db.cursor()
    #c_plat 是平台的中文名称
    
    #返回自增id
    def store_data(self,data,c_plat):  
        sql1 = "set names utf8"
        sql = """INSERT INTO article(tag,title,url,author,avatar_url,views,hot,time,platform,info)\
        VALUES ("[]","{}","{}","{}","{}",{},{},'{}','{}','{}')"""\
        .format(data['title'],data['url'],data['author'],data['avatar_url'],data['views'],data['hot'],data['time'],c_plat,data['info'])
        #记录热度基数
        try:
            self.cursor.execute(sql1)
            self.cursor.execute(sql)
            self.db.commit()
        except:
            traceback.print_exc()
            self.db.rollback()
            self.db.close()
            exit()
        return self.cursor.lastrowid
    #存储热度
    def store_hot(self,p,hot_sum):
        sql = "insert into hot(platform,hot_sum,item_num) values('{}',{},{}) ON DUPLICATE KEY update hot_sum=hot_sum+{},item_num=item_num+{}".format(p,hot_sum,1,hot_sum,1)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            traceback.print_exc()
            self.db.rollback()
            self.db.close()
            exit()
    #存储标签统计
    
    #在tag表里面计数标签
    def store_tag_in_tag(self,tag):
        tag = self.rm_tag(tag)
        for t in tag:
            sql = """insert into tag(number,item) values({},"{}") ON DUPLICATE KEY update number=number+1""".format(1,t)
            self.cursor.execute(sql)
        self.db.commit()  
    
    #在文章表中存储标签
    def store_tag_in_article(self,tag,id): 
        tag = self.rm_tag(tag)     
        sql = """update article set tag = "{}" where id={}""".format(tag,id)
        self.cursor.execute(sql)
        self.db.commit()   
    #存储文本数据   
    
    
    #在文章表中存储标签
    def store_tag_in_content_text(self,tag,id): 
        tag = self.rm_tag(tag)     
        sql = 'update content_text set keywords = "{}" where id={}'.format(tag,id)
        self.cursor.execute(sql)
        self.db.commit()   
    #存储文本数据   
    
    def store_text(self,text,id,title):
        
        sql1 = "SET NAMES utf8"
        sql = """INSERT INTO content_text(id,title,content)\
        VALUES ({},"{}","{}")"""\
        .format(id,title,text)
        self.cursor.execute(sql1)
        self.cursor.execute(sql)
        self.db.commit()
    #特殊tag去重
    
    def rm_tag(self,tag):
        for i in range(len(tag)):
            if tag[i]=="区块" or tag[i]=="区块链(Blockchain)":
                tag[i]="区块链"
            if tag[i]=="比原" or tag[i]=="bytom" or tag[i]=="Bytom" or tag[i]=="比原链Bytom":
                tag[i]="比原链"
            if tag[i]=="比特" or tag[i]=="比特币 (Bitcoin)":
                tag[i]="比特币"
            if tag[i]=="资本":
                tag[i]="资产"
        return tag
