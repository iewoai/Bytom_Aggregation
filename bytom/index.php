<?php
  session_start();
  #设置sessionid
  $_SESSION['flag'] = md5(uniqid(microtime(true),true));
  #文本推荐标签
  require_once "lib/mysql_conn.php";
?>

<!DOCTYPE HTML>
<html lang="zh-CN">
<head>
  <meta name="referrer" content="never">
<meta charset="utf-8">
<meta name="applicable-device" content="pc,mobile">
<meta http-equiv="Cache-Control" content="no-transform" />
<meta http-equiv="Cache-Control" content="no-siteapp" />
<meta http-equiv="X-UA-Compatible" content="ie=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=0, minimum-scale=1.0, maximum-scale=1.0">
<title>Bytom信息聚合</title>
<meta name="description" content="" />
<meta name="keywords" content="" />
<meta name="author" content="order by dede58.com" />
<link rel="canonical" href=""/>
<link rel='stylesheet' href='public/style.css' type='text/css' media='all' />

<style type="text/css">

</style>
</head>
<body>
<header class="header" style="position: fixed">
  <div class="container">
    <h2 class="logo logo-m"><span style='color:white'>『</span><img style='width:30px' src='public/logo.png'><span style='color:white'>』</span></h2>
    <div class="brand pc">Bytom信息聚合平台</div>
    <ul class="nav nav-m">
      <li id="nvabar-item-index"><a href="">首页</a></li>
      <li><a onclick="get_data(1,'time')">最新</a></li>
      <li><a onclick="get_data(1,'hot')">最热</a></li>

      <li>
        <select onchange="get_data(1,'platform')">
          <option value="全部">全部</option>
          <?php
              $conn = mysql_conn::create_mysql();
              $sql = "select platform from hot";
              if($data = $conn->select($sql)){
                  for($i=0;$i<sizeof($data);$i++){
                      $v = $data[$i]['platform'];
                      echo "<option value='$v'>$v</option>";
                  }
                  
              }

          ?>   
        </select>
      </li>

      <li><input type='text' id="search">&nbsp<input id='search_btn' type="button" onclick="search(1)" value='搜索'></li>
    </ul>
  </div>
</header>

<section class="container" style="margin-top:100px">

  <div class="content-wrap">
    <div class="content"> 

      <article class="excerpt-see excerpt-see-index pc" id="recommend"> 
        

      </article>

      <div id="article_content">
        
      </div>
    
      <div style="clear:both"></div>
      <div class="cygswtags tags">
        <ul>
          <?php
            $sql="select item,number from tag order by number desc";
            $j=1;
            if($res = $conn->select($sql)){
              for($i=0;$i<sizeof($res);$i++){
                $item = $res[$i]['item'];
                $number = $res[$i]['number'];
                echo "<li><a onclick='get_data(1,\"tagFlag_$item\")'>$item($number)</a></li>";
                if($j==15){
                  break;
                }
                $j++;
              }
            }
          ?>
        </ul>
      </div>

    </div>
  </div>

  <aside class="sidebar pc" style="position: fixed;margin-left:920px">
    <dl class="function" id="tishi">
      <dt class="function_t">关于本站</dt>
      <dd class="function_c">
        <div> 网站简介 - 代码改变世界 Coding Changes the World 欢迎来到bytom新闻聚合网站，我们不提供新闻，我们只是新闻的搬运工!
        </div>
      </dd>
    </dl>

    <dl class="function" id="divPrevious" >
      <dt class="function_t">最近发表</dt>
      <dd class="function_c">
        <ul>
          <?php
            $sql = "select title,url from article order by time desc limit 0,8";
            $res = $conn->select($sql);
            if($res){
              for($i=0;$i<sizeof($res);$i++){
                $url = $res[$i]['url'];
                $title = $res[$i]['title'];
                echo"<li><a href='$url' target='_blank'>$title</a></li>";
              }
            }
          ?>
      
        </ul>
      </dd>
    </dl>
  </aside>
</section>

<footer class="footer" id="footer">
  <div class="container">
    <p>粤ICP备32323659号</p>
    <p>Copyright &copy; 2002-2017 www.setsails.cn 版权所有 <a href="www.setsails.cn/bytom" target="_blank">Power by fang</a></p>
    
  </div>
</footer>

</body>

<script type="text/javascript" src="public/jquery.js"></script>
<script type="text/javascript">
  get_data(1,'time')
  function get_data(page,sort_type){
    $.ajax({
      url:'get_data.php',
      data:{"page":page,"sort_type":sort_type,"platform":$("select option:selected").val()},
      type:"get",
      dataType:"text",
      success:function(res){
        $("#article_content").html(res);
      }
    })
  }


  function search(page){
    $.ajax({
      url:'search.php',
      data:{"info":$('#search').val(),"page":page},
      type:"get",
      dataType:"text",
      success:function(res){
        $("#article_content").html(res);
      }
    }
    )  
  }


  function recommend(id){
    $.ajax({
      url:'recommend.php',
      data:{"id":id},
      type:"get",
      dataType:"text",
      success:function(res){
        $("#recommend").html(res);
      }
    }
    )  
  }
</script>
</html>