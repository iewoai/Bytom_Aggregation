<?php
	class get_html{
		#输出html文章数据
		function echo_article($id,$title,$url,$author,$avatar_url,$views,$tag,$platform,$time,$info){
			$time = date("Y/m/d",$time);
			$tag = eval("return $tag;");

			$str = "";
			for($i=0;$i<sizeof($tag);$i++){
				$str.="<time style='color:blue'>$tag[$i]</time>";
			}
		
	      return "<article class='excerpt' onclick='recommend($id)'>
	      			<header>
          				<a target='_blank' href='$url' class='cat'>$platform</a>
          				<h2>
            				<a target='_blank' href='$url'>$title</a>
          				</h2>
        			</header>
        			<a target='_blank' class='focus' href='$url' >
          				<img src='$avatar_url' />
        			</a>
        			<p class='meta'>
          				<time>By $author</time>
	          			<time>$time</time>
	          			<span class='pv'>阅读($views)</span> </p>
          			</p>
        			<p class='note pc'> <a style='display:block;width:100%;height:50px;overflow:hidden' target='_blank' href='$url'>  $info</a></p>
        			</p>
        			<p class='meta'>
	           			$str
	        		</p>
      			</article>";
		}

	}