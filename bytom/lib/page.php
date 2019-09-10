<?php
	class page{
		public function __construct($page,$article_num,$page_num,$limit,$sort_type,$function){
			$this->page = $page;
			$this->article_num = $article_num;
			$this->page_num = $page_num;
			$this->limit = $limit;
			$this->sort_type = $sort_type;
			$this->function = $function;

		}
		#输出html代码
		#$page当前页码,$article_num数据总数，$limit每一页显示数据数量,$page_num每个网页显示的页数
		function echo_page(){
			#总页数
			$page_count = ceil($this->article_num/$this->limit);
			$html='<div style="text-align:center">
	        <div style="display:inline-block;margin-top:20px">';
	          
			if($this->page_num%2!=0){
				$left=$this->page_num/2;
				$right = $left;
			}else{
				$left = ceil($this->page_num/2)-1;
				$right=$left+1;
			}
			$left = ceil($this->page_num/2)-1;
			#一共存在3种情况的分页
			if($page_count<=$this->page_num){
				if($this->page!=1){
					$p = $this->page-1;
					$html.="<div class='page next_pre' onclick='{$this->function}($p,\"{$this->sort_type}\")'>上一页</div>";
				}
				for($i=1;$i<=$page_count;$i++){
					if($i==$this->page){
						$html .= "<div class='page' style='background:gray'>$i</div>";
					}else{
						$html .= "<div class='page' onclick='{$this->function}($i,\"{$this->sort_type}\")'>$i</div>";
					}
				}
				if($this->page!=$page_count){
					$p = $this->page+1;
					$html.="<div class='page next_pre'  onclick='{$this->function}($p,\"{$this->sort_type}\")'>下一页</div>";
				}
			}else{
				if($this->page-$left<=0){
					$p=$this->page-1;
					$html.="<div class='page next_pre' onclick='{$this->function}($p,\"{$this->sort_type}\")'>上一页</div>";
					for($i=1;$i<=$this->page_num;$i++){
						if($i==$this->page){
							$html .= "<div class='page' style='background:gray'>$i</div>";
						}else{
							$html .= "<div class='page' onclick='{$this->function}($i,\"{$this->sort_type}\")'>$i</div>";
						}
					}
					$p = $this->page+1;
					$html.="<div class='page next_pre'  onclick='{$this->function}($p,\"{$this->sort_type}\")'>下一页</div>";
					
				}else if($page_count-$this->page<$right){
					$p = $this->page-1;
					$html.="<div class='page next_pre' onclick='{$this->function}($p,\"{$this->sort_type}\")'>上一页</div>";
					for($i=$page_count-$this->page_num+1;$i<=$page_count;$i++){
						if($i==$this->page){
							$html .= "<div class='page' style='background:gray'>$i</div>";
						}else{
							$html .= "<div class='page' onclick='{$this->function}($i,\"{$this->sort_type}\")'>$i</div>";
						}
					}
					if($this->page!=$page_count){
						$p = $this->page+1;
						$html.="<div class='page next_pre' onclick='{$this->function}($p,\"{$this->sort_type}\")'>下一页</div>";
					}
				}else{
					$p = $this->page-1;
					$html.="<div class='page next_pre'  onclick='{$this->function}($p,\"{$this->sort_type}\")'>上一页</div>";
					for($i=$this->page-$left;$i<=$this->page+$right;$i++){
						if($i==$this->page){
							$html .= "<div class='page' style='background:gray'>$i</div>";
						}else{
							$html .= "<div class='page' onclick='{$this->function}($i,\"{$this->sort_type}\")'>$i</div>";
						}
					}
					$p = $this->page+1;
					$html.="<div class='page next_pre' onclick='{$this->function}($p,\"{$this->sort_type}\")'>下一页</div>";
				}
			}

			return $html.'</div></div>';
		}
	}