<?php
	header("Content-type: text/html; charset=utf-8");
	$info="侧链技术现状了";
	#下面的 2>&1表示输出错误信息
	
    $program="PYTHONIOENCODING=utf-8 python3 ./python/lib/text.py {$info} 2>&1"; 
    print(shell_exec($program));

	
    
    
