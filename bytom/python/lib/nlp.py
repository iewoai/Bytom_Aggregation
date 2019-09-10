#coding=utf-8
import jieba, re
import jieba.analyse
import jieba.posseg as psg
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.feature_extraction.text import TfidfTransformer  
import os
class nlp:
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        
    #获取停用词列表
    def get_stop_words(self):
        stopwords = []
        for word in open(self.path+"/STOPWORDS.txt", "r",encoding="utf-8"):
            stopwords.append(word.strip())
        return stopwords
    
    #获取分词
    def get_cut(self,content):
        content = re.sub(r'\s|\n', '', content)
        jieba.initialize()
        jieba.load_userdict(self.path+"/dict.txt")
        jieba.add_word("比原链")
        jieba.add_word("区块链")
        jieba.add_word("以太坊")
        res = psg.cut(content)
        stop_words = self.get_stop_words()
        words_list = []
        allowPOS=('n','nr','ns','nt','nz','v','a','vn','eng')
        for i in res:
            if i.word.lower() not in [current.lower() for current in stop_words] and i.flag in allowPOS:
                words_list.append(i.word)
        return " ".join(words_list)
    
    
    
    #获取关键字
    def get_keywords(self,text_list):
        #该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频  
        vectorizer=CountVectorizer()
        #该类会统计每个词语的tf-idf权值  
        transformer=TfidfTransformer()
        #第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵  
        tfidf=transformer.fit_transform(vectorizer.fit_transform(text_list))
        #获取词袋模型中的所有词语  
        word=vectorizer.get_feature_names()
        #将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重  
        weight=tfidf.toarray()
        #打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        key_dict={}  
        for i in range(len(weight)):
            #print ("每篇文章前20权重的关键字") 
            res = []
            for j in range(len(word)):  
                key_dict[word[j]]=weight[i][j]
            key_words = sorted(key_dict.items(),key=lambda x:x[1],reverse=True)
            
            for j in key_words[0:20]:
                res.append(j[0])
            yield res
            res= []
            key_dict={} 