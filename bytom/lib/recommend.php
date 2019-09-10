<?php
	if(!isset($_GET['id'])){
		die();
	}

	#调用推荐系统
	$id = $_GET['id'];
	#下面的 2>&1表示输出错误信息
	$id = urlencode($id);
    $program="PYTHONIOENCODING=utf-8 python3 ./python/lib/recommend.py {$id} 2>&1";

	$redis = new Redis();
	$redis->connect("localhost",6379);
	$res = $redis->hGet('recommend',$_GET['id']);


	//获取推荐结果
	$html = ""; 
	if($res){
		//已经有结果
		$id_list = eval("return $res;");
		$mysql = new Mysqli("localhost","root","fang","bytom");
		$f_id = $id_list[0];
		$sql = "select id,title,info,url from article where id=$f_id";
		$data = $mysql->query($sql);
		$data = $data->fetch_all(MYSQLI_ASSOC)[0];
		$html = $html."<h2><span class='red'>【站长推荐】</span> 
          <a href='$data['url']' onclick='recommend($data['id'])'>$data['title']</a></h2>
        <p class='note'> <a href='$data['url']'>$data['info']</a></p><div class='relatescom'><ul>";
		for($i=1;$i<sizeof($id_list);$id++){
			$sql = "select id,title,info,url from article where id=$i";
			$data = $mysql->query($sql);
			$data = $data->fetch_all(MYSQLI_ASSOC)[0];
			$html = $html."<li><a href='$data['url']' onclick='recommend($data['id'])'>$data['title']</a></li>";
		}
		$html = $html."</ul></div>";
	}

