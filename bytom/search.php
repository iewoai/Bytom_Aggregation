<?php
    header("Content-type:text/html;charset=utf-8");
	session_start();
	
	require_once "./lib/page.php";
	require_once "./lib/get_html.php";
 	#设置sessionid
  	
	if(!isset($_SESSION['flag'])||!isset($_GET['page'])){
		die("请刷新页面");
	}
	
	$info = $_GET['info'];
	#下面的 2>&1表示输出错误信息
	$info = urlencode($info);
    $program="PYTHONIOENCODING=utf-8 python3 ./python/lib/search.py {$info} {$_SESSION['flag']} 2>&1";

    if(!isset($_SESSION['search'])||$_SESSION['search']!=$info){
    	exec($program);
    	$_SESSION['search'] = $info;
    } 
    	
    

    #操作redis
	$redis = new Redis();
	$redis->connect('127.0.0.1', 6379);
	$str = $redis->get($_SESSION['flag']);

	$id_list = eval("return $str;");
	

	$page=$_GET['page'];
	$offset = ($page-1)*10;
	#查询数据
	$conn = new mysqli("localhost","root","fang","bytom");
	$res = $conn->query("set names utf8");
	$html = "";
	$get_html = new get_html();
	$j=0;
	for($i=$offset;$i<sizeof($id_list);$i++){
		if($j==10){
			break;
		}
		$j++;
		$id = $id_list[$i];
		$sql = "select id,hot,title,url,author,avatar_url,views,tag,platform,time,info from article where id=$id";
		$res = $conn->query($sql);
		$res = $res->fetch_all(MYSQLI_ASSOC);
		$data = $res[0];

		$html .= $get_html->echo_article($data['id'],$data['title'],$data['url'],$data['author'],$data['avatar_url'],$data['views'],$data['tag'],$data['platform'],$data['time'],$data['info']);
	}

	$page = new page($page,sizeof($id_list),10,10,"","search");
	$html = $html.$page->echo_page();
    echo $html;
    
