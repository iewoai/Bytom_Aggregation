<?php
	class mysql_conn{
		//单例模式
		static $conn;
		static $mysql;
		protected function __construct(){
			
		}
		public static function create_mysql(){
			if(!self::$mysql){
				self::$conn = new Mysqli('localhost','root','fang','bytom');
				if(self::$conn->connect_error){
					die("数据库连接失败");
				}
				self::$mysql = new self();
			}
			return self::$mysql;
		}
		public function select($sql){
			self::$conn->query("set names utf8");
			$result = self::$conn->query($sql);
			if($result->num_rows>0){
				//返回一个数组
				return $result->fetch_all(MYSQLI_ASSOC);
			}else{
				return 0;
			}
		}
		
		public function add_update_delete($sql){
			self::$conn->query("set names utf8");
			if(self::$conn->query($sql)){
				return 1;
			}else{
				return 0;
			}
		}

		
	}	

?>