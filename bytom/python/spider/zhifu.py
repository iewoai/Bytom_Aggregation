#coding=utf-8
import sys
sys.path.append("..")
import requests
import random
import re
import time
from lib import setting
import json
from lxml import etree
import html
import os

class zhifu:
    def __init__(self):
        
        #开启会话
        headers = {"USER-AGENT":random.choice(setting.user_agent_list),}
        self.session = requests.session()
        self.session.get("https://www.zhihu.com/search?q=bytom&type=content",verify=False,headers=headers)
        
        #载入去重数据
        self.path = os.path.dirname(os.path.abspath(__file__))
        file = open(self.path+"/../lib/zhifu.txt","r")
        self.s = set(file.readline().split(" "))
        file.close()
    
    def send_request(self,url,headers={"USER-AGENT":random.choice(setting.user_agent_list)},method=None):
        #发送请求获取response
        headers={"USER-AGENT":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
        try:
            if(method=="post"):
                response = self.session.post(url,verify=False,headers=headers,timeout=(4,4))
            else:
                response = self.session.get(url,verify=False,headers=headers,timeout=(4,4))
        except requests.exceptions.ConnectTimeout:
            print("请求超时")
            return 0
        except requests.exceptions.ReadTimeout:
            print("下载超时")
            return 0
        else: 
            response.encoding='utf-8'
            return response
        
        #处理每一页
    def get_single_page_data(self,res):
        for i in res['data']:
            #判断是文章还是问答
            item = {}
            if(i['object']['type']=="answer"):
                if(self.rm_repeated("an"+i['object']['question']['id'])):
                    yield 0
                    continue
                item['author'] = "default"
                item['avatar_url'] = "default"
                item['views'] = 0
                item['likes'] = 0
                item['type'] = "answer"
                item['comments'] = 0
                item['url'] = "https://www.zhihu.com/question/"+i['object']['question']['id']
            else:
                if(self.rm_repeated(("ar"+i['object']['id']))):
                    yield 0
                    continue
                item['author'] = i['object']['author']['name']
                item['avatar_url'] = i['object']['author']['avatar_url']
                item['comments'] = i['object']['comment_count']
                item['likes'] = i['object']['voteup_count']
                item['type'] = "article"
                item['views'] = 0
                item['url'] = "https://zhuanlan.zhihu.com/p/"+i['object']['id']    
            item['title'] = self.rm_html(i['highlight']['title'])
            item['time'] = i['object']['updated_time']
            item['text'] = "default"
            item['collections']=0
            item['imgs_num'] = 0
            #深入访问连接
            yield self.get_article_data(item)
            
    
#进入文章连接获取数据
    
    def get_article_data(self,item):
        #进入文章链接，获取文本.
        res = self.send_request(item['url'],method="get")
        tree = etree.HTML(res.text)
        #提取标签
        tag = tree.xpath("//a[@class='TopicLink']/div/div")
        item['tag']=[]
        for t in tag:
            item['tag'].append(t.text)
        #文章处理
        if item['type'] == "article":
            article = tree.xpath("//article")[0]
            str1 = html.unescape(etree.tostring(article).decode("utf-8"))
            #统计img数量
            item['imgs_num'] = len(re.findall("<img",str1))
            item['text'] = self.rm_html(str1)
            item['views'] = item['comments']*2+item['likes']*2+item['collections']*2
        #问答模式处理   
        else:
            #获取浏览量
            item['views'] = tree.xpath("//strong[@class='NumberBoard-itemValue']")[1].text
            item['views'] = int(re.sub(",","",item['views']))
            #获取全部回答数量
            next_url = "https://www.zhihu.com/api/v4/questions/"+str(item['url'].split("/")[-1])+"/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=0&platform=desktop&sort_by=default"
            res = self.get_json(next_url)
            
            while(len(res['data'])>0):
                for data in res['data']:
                    item['text']=item['text']+self.rm_html(data['content'])
                    item['imgs_num'] = item['imgs_num']+len(re.findall('<img',data['content']))
                    item['comments'] = item['comments']+data['comment_count']
                    item['likes'] = item['likes']+data['voteup_count']
                item['imgs_num'] = item['imgs_num']/2    
                next_url = res['paging']['next']
                res = self.get_json(next_url)
        item['hot'] = item['imgs_num']*0.7+item['views']*1+item['likes']*1.5+item['comments']*2+item['collections']*2.5
        #将标题加入文本
        item['info'] = item['text'][0:75]
        
        return item
         
    #获取一个完整的item
    
    def get_data(self):
        url = "https://www.zhihu.com/api/v4/search_v3?t=general&q=bytom&correction=1&offset=0&limit=20&lc_idx=21&show_all_topics=0&search_hash_id=e8f330d45ca2fb5d2ae38d36eb76e4ed&vertical_info=0%2C1%2C1%2C0%2C0%2C0%2C0%2C0%2C0%2C0"
        res = self.get_json(url)
        while len(res['data'])>0:
            items = self.get_single_page_data(res)
            for item in items:
                #判断是否到末尾
                if(item==0):
                    continue
                #处理每一个item
                yield item
            res = self.get_json(res['paging']['next'])
                   
    def rm_html(self,str1): 
        str1 = re.sub("<svg[\s\S]*?</svg>","",str1)
        return re.sub('<[^<]+?>', '', str1).replace('\n', '').strip() 
       
    def write_item(self,text,title):
        with open("test.txt","a",encoding='utf-8') as f:
            f.write(title+"\n"+text+"\n\n\n")
    
    #去重
    def rm_repeated(self,str1):
        #去重处理
        if str1  not in self.s:
            with open(self.path+"/../lib/zhifu.txt","a") as f:
                f.write(str1+" ")
                f.close()
                self.s.add(str1)
            return 0
        else:
            print("跳过"+str1)
            time.sleep(0.1)
            return 1
    
    #获取json文件
    def get_json(self,url):
        headers = {"USER-AGENT":random.choice(setting.user_agent_list),"Accept":"application/json"}
        res = self.send_request(url,headers=headers,method="get")
        return json.loads(res.text)
    
    def get_newest_data(self):
        url = "https://www.zhihu.com/api/v4/search_v3?t=general&q=bytom&correction=1&offset=0&limit=20&lc_idx=51&show_all_topics=0&time_zone=three_months&search_hash_id=eddc53528ca0fe7ebd71a8e00d70dc55&vertical_info=0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0"
        res = self.get_json(url)
        if len(res['data'])>0:
            item = self.get_single_page_data(res)
            for i in item:
                if i !=0:
                    yield i
                    
                    
                    
if __name__ == '__main__':
    zhifu = zhifu()
    #zhifu.get_newest_data()
    res = zhifu.get_data()
    for i in res:
        pass
    