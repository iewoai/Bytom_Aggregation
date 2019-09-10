#coding=utf-8
import requests
import random
import re
import time
from lib import setting
import json
from lxml import etree
import html
import os
class jianshu:
    def __init__(self):
        #开启会话
        headers = {"USER-AGENT":random.choice(setting.user_agent_list),}
        self.session = requests.session()
        self.session.get("https://www.jianshu.com/search?q=bytom&page=1&type=note",verify=False,headers=headers)
        
        #载入去重数据
        self.path = os.path.dirname(os.path.abspath(__file__))
        file = open(self.path+"/../lib/jianshu.txt","r")
        self.s = set(file.readline().split(" "))
        file.close()
    def send_request(self,url,headers={"USER-AGENT":random.choice(setting.user_agent_list)},method=None):
        #发送请求获取response

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
        
    #去除字符串中的html标签
    def rm_html(self,str1): 
        return re.sub('<[^<]+?>', '', str1).replace('\n', '').strip()
    #提取单页数据
    def get_single_page_data(self,url):
        headers = {"USER-AGENT":random.choice(setting.user_agent_list),"Accept":"application/json"}
        
        response = self.send_request(url,headers,method="post")
        res = json.loads(response.text)['entries']
        for i in range(len(res)):
            #去重处理
            if res[i]['slug']  not in self.s:
                with open(self.path+"/../lib/jianshu.txt","a") as f:
                    f.write(res[i]['slug']+" ")
                    f.close()
                self.s.add(res[i]['slug'])
            else:
                print("跳过"+self.rm_html(res[i]['title']))
                time.sleep(0.5)
                continue
            item = {}
            p_time = res[i]['first_shared_at'].replace("T"," ").replace(".000Z","")
            
            item['title'] = self.rm_html(res[i]['title'])
            item['url'] = "https://www.jianshu.com/p/"+res[i]['slug']
            item['time'] = int(time.mktime(time.strptime(p_time, "%Y-%m-%d %H:%M:%S")))
            item['views'] = res[i]['views_count']
            item['comments'] = res[i]['public_comments_count']
            item['likes'] = res[i]['likes_count']
            item['author'] = self.rm_html(res[i]['user']['nickname'])
            item['avatar_url']=res[i]['user']['avatar_url']
            #获取文本信息
            response = self.send_request(item['url'],method = "get").text
            tree = etree.HTML(response)
            div = tree.xpath('//div[@class="show-content"]')[0]
            str1 = etree.tostring(div).decode("utf-8")
            
            #文本需要连接上标题
            item['text'] = self.rm_html(html.unescape(str1))
            #获取文本前几句
            item['info'] = item['text'][0:75]
            #文本需要连接上标题
            item['text'] = item['title']+self.rm_html(html.unescape(str1))

            #统计文本图片数量
            item['imgs_num'] = len(div.xpath("img"))
            
            #计算热度
            item['hot'] = item['views']*1+item['comments']*2+item['imgs_num']*0.7+item['likes']*1.5
            item['text'] = item['text']+item['title']
            
            yield item
    def get_data(self):
        #cookies="__yadk_uid=cR1keDyfrOrUKkWaHc9zVUCkygz7jNUk; read_mode=day; default_font=font2; locale=zh-CN; _m7e_session_core=39ddaf6ea7c475abe8d32c9a737796fa; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1556030484,1556033477,1556033732,1556078591; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22167014ba1351a9-02e92aabed5fbc-5c11301c-1327104-167014ba136146%22%2C%22%24device_id%22%3A%22167014ba1351a9-02e92aabed5fbc-5c11301c-1327104-167014ba136146%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; signin_redirect=https%3A%2F%2Fwww.jianshu.com%2Fsearch%3Fq%3Dbytom%26page%3D1%26type%3Dnote; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1556088553"
        #cookies = {i.split("=")[0].strip():i.split("=")[1] for i in cookies.split(";")}
        for j in range(26):
            url = "https://www.jianshu.com/search/do?q=bytom&type=note&page="+str(j+1)+"&order_by=published_at"
            item = self.get_single_page_data(url)
            for i in item:
                yield i

    #获取最新数据
    def get_newest_data(self):
        url = "https://www.jianshu.com/search/do?q=bytom&type=note&page=1&order_by=published_at"
        data = self.get_single_page_data(url)
        for i in data:
            yield i
            
if __name__ == '__main__':
    jianshu = jianshu()
    res = jianshu.get_data()
    #res = jianshu.get_newest_data()
    j=1
    for i in res:
        print(str(j)+"  "+i['title']+"  "+str(i['hot'])+"  "+str(i['hot_sum'])+"  "+str(i['item_num']))
        j=j+1
    

    
    