<?php
	if(!isset($_GET['id'])){
		die();
	}

	#调用推荐系统
	$id = $_GET['id'];
	#下面的 2>&1表示输出错误信息
	$id = urlencode($id);
    $program="PYTHONIOENCODING=utf-8 python3 ./python/lib/recommend.py {$id} 2>&1";
    exec($program);

	$redis = new Redis();
	$redis->connect("localhost",6379);
	$res = $redis->hGet('recommend',$_GET['id']);


	//获取推荐结果
	$html = ""; 
	$mysql = new Mysqli("localhost","root","fang","bytom");
	$mysql->query("set names utf8");
	if($res){
		//已经有结果
		$id_list = eval("return $res;");
		
		$f_id = $id_list[0];
		$sql = "select id,title,info,url from article where id=$f_id";
		$data = $mysql->query($sql);
		$data = $data->fetch_all(MYSQLI_ASSOC);
		$html = $html."<h2><span class='red'>【站长推荐】</span> 
          <a target='_blank' href='".$data[0]['url']."' onclick='recommend(".$data[0]['id'].")'>".$data[0]['title']."</a></h2><p class='note' style='margin-left:10px'><a target='_blank' href='".$data[0]['url']."'>".$data[0]['info']."</a></p><div class='relatescom'><ul>";
		for($i=1;$i<sizeof($id_list);$i++){
			$id = $id_list[$i];
			$sql = "select id,title,info,url from article where id=$id";
			$data = $mysql->query($sql);
			$data = $data->fetch_all(MYSQLI_ASSOC);
			$html = $html."<li><a target='_blank' href='".$data[0]['url']."' onclick='recommend(".$data[0]['id'].")'>".$data[0]['title']."</a></li>";
		}
		$html = $html."</ul></div>";
	}
	echo $html;

