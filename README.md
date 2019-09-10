# Bytom_Aggregation
bytom新闻聚合网站，爬取知乎、巴比特、csdn、简书上与bytom有关的内容

一、文档结构树

    /.
    │  treefile.txt #原文档结构树
    │  README.md
    │  LICENSE
    │  
    └─bytom
        │  get_data.php #获取data
        │  index.php #主页
        │  mysql_conn.php #连接数据库
        │  recommend.php #推荐
        │  search.php #查找
        │  test.php #测试
        │  
        ├─lib
        │      get_html.php #输出文章数据到网页
        │      mysql_conn.php #连接数据库
        │      page.php #页码
        │      recommend.php #推荐
        │      
        ├─public #样式
        │      jquery.js
        │      logo.png
        │      style.css
        │      
        └─python
            │  dispatcher.py #热度排序
            │  
            ├─lib 
            │  │  dict.txt
            │  │  jianshu.txt
            │  │  nlp.py #分词
            │  │  recommend.py #推荐
            │  │  search.py #查找
            │  │  setting.py #环境设置
            │  │  STOPWORDS.txt #分词词库
            │  │  store_data.py #切割并储存数据
            │  │  zhifu.txt
            │  │  __init__.py
            │  │  
            │  └─__pycache__
            │          nlp.cpython-35.pyc
            │          setting.cpython-35.pyc
            │          store_data.cpython-35.pyc
            │          __init__.cpython-35.pyc
            │          
            └─spider #爬虫文件
                │  bit.py #巴比特爬虫
                │  csdn.py #csdn爬虫
                │  jianshu.py #简书爬虫
                │  zhifu.py #知乎爬虫
                │  __init__.py
                │  
                └─__pycache__
                        bit.cpython-35.pyc
                        csdn.cpython-35.pyc
                        jianshu.cpython-35.pyc
                        setting.cpython-35.pyc
                        zhifu.cpython-35.pyc
                        __init__.cpython-35.pyc