<?php
		require './lib/page.php';
		require './lib/get_html.php';
		$conn = new mysqli("localhost","root","fang","bytom");
		if($conn->connect_error){
			die("数据库连接失败");
		}
		$conn->query("set names utf8");

		if(!isset($_GET['page'])||!isset($_GET['sort_type'])||!isset($_GET['platform'])){
			die("参数错误");
		}
		$page = $_GET['page']; 
		$sort_type = $_GET['sort_type'];
		$platform = $_GET['platform'];
		

		echo get_data($page,$conn,$sort_type,$platform,10,7);

		
		
		#获取数据
		#$limit每一页的数据量
		#$page当前页数
		#$page_num每个网页显示的页数
		function get_data($page,$conn,$sort_type,$platform,$limit,$page_num){
			$sql_str = "select id,hot,title,url,author,avatar_url,views,tag,platform,time,info from ";
			#计算文章数量
			if($platform!="全部"){
				$sql = "select count(*) from article where platform=?";
				$stmt = $conn->prepare($sql);
				$stmt->bind_param("s",$platform);
				$stmt->execute();
				$stmt->bind_result($article_num);
				$stmt->fetch();
				$stmt->close();
			}else if(explode("_",$sort_type)[0]=="tagFlag"){
				$sql = "select count(*) from article where tag like ?";
				$stmt = $conn->prepare($sql);
				$str = "%".explode("_",$sort_type)[1]."%";
				$stmt->bind_param("s",$str);
				$stmt->execute();
				$stmt->bind_result($article_num);
				$stmt->fetch();
				$stmt->close();
			}else{
				$sql = "select count(*) from article";
				$res = $conn->query($sql);
				$res = $res->fetch_all(MYSQLI_ASSOC);
				$article_num = $res[0]['count(*)'];
			}
			
			#计算偏移量
			if(is_numeric($page)){
				$offset = (intval($page)-1)*$limit;
				if($offset>=$article_num){
				#已经是最后一页
					die("没有更多的数据了");
				}
			}else{
				die("提交数据有误");
			}

			#按照时间和平台排序
			if($sort_type=="time"&&$platform!="全部"){
				$sql = $sql_str."article where platform=? order by time desc limit ?,$limit";
				$stmt = $conn->prepare($sql);
				$stmt->bind_param("si",$platform,$offset);
			}else if($sort_type=="hot"&&$platform!="全部"){
				#按照平台和热度排序
				$sql = $sql_str."article where platform=? order by hot desc limit ?,$limit";
				$stmt = $conn->prepare($sql);
				$stmt->bind_param("si",$platform,$offset);
			}else if($sort_type=="time"){
				#只按照时间排序
				$sql = $sql_str."article order by time desc limit ?,$limit";
				$stmt = $conn->prepare($sql);
				$stmt->bind_param("i",$offset);
			}else if($sort_type=="hot"){
				#只按照热度排序
				$sql = "select platform,hot_sum,item_num from hot";
				$res = $conn->query($sql);
				$res = $res->fetch_all(MYSQLI_ASSOC);
				$sql="";
				#联合查询
				for($i=0;$i<sizeof($res);$i++){
					$avg = $res[$i]['hot_sum']/$res[$i]['item_num'];
					$platform = $res[$i]['platform'];
					if($i==sizeof($res)-1){
						$sql .="(select id,hot/$avg as hot, title,url,author,avatar_url,views,tag,platform,time,info from article where platform='$platform') order by hot desc limit ?,$limit";
					}else{
						$sql .="(select id,hot/$avg as hot, title,url,author,avatar_url,views,tag,platform,time,info from article where platform='$platform') union ";
					}	
				}
				$stmt = $conn->prepare($sql);
				$stmt->bind_param("i",$offset);
			}else if($sort_type=="platform"&&$platform!="全部"){
				#只按照平台排序
				$sql = $sql_str."article where platform=? order by time desc limit ?,$limit";
				$stmt = $conn->prepare($sql);
				$stmt->bind_param("si",$platform,$offset);
			}else if($platform=="全部"){
				#只按照全部排序
				$sql = $sql_str."article order by time desc limit ?,$limit";
				$stmt = $conn->prepare($sql);
				$stmt->bind_param("i",$offset);
			}else if(explode("_",$sort_type)[0]=="tagFlag"){
				#根据标签排序
				$sql = $sql_str."article where tag like ? order by time desc limit ?,$limit";
				$stmt = $conn->prepare($sql);
				$str = "%".explode("_",$sort_type)[1]."%";
				$stmt->bind_param("si",$str,$offset);
			}else{
				die("操作错误");
			}

			$stmt->execute();
			$stmt->bind_result($id,$hot,$title,$url,$author,$avatar_url,$views,$tag,$platform,$time,$info);
			$html="";
			$get_html = new get_html();
			while($stmt->fetch()){
				$html .= $get_html->echo_article($id,$title,$url,$author,$avatar_url,$views,$tag,$platform,$time,$info);
			}
			$page = new page($page,$article_num,$page_num,$limit,$sort_type,"get_data");
			$html.=$page->echo_page();
			return $html;
			
		}

		
		
	

	#


	
	