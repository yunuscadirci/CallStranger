<?php
 error_reporting(E_ALL & ~E_NOTICE);
if ($_REQUEST['token'])
	session_id($_REQUEST['token']);
session_start();
switch ($_GET["c"]) {
    case "getsession":
        echo session_id();
        break;
    case "addservice":
       if (!isset($_SESSION['services'])) {
		$_SESSION['services'] = array(); 		}
	   if(count($_SESSION['services'])<50)		{
		array_push($_SESSION['services'],$_GET["service"]);
		echo "1"; 		}
	   else 		{		echo "0";		}
        break;
    case "getservices":
		foreach($_SESSION['services'] as $s){
    echo $s. PHP_EOL; }
        break;
	}
?>