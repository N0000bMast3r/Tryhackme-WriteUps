<html>
<title>Login</title>
<body style="background-color:black">
<br><br><br>
<h3 style="color:red;text-align:center">Bank Of Abc Def User Login</h3>
<br>
<style>
form{
  border: 2px solid black;
  outline: #4CAF50 solid 3px;
  margin: auto;
  width:180px;
  padding: 20px;
  text-align: center;
}
</style>
<form method="POST" style="text-align:center" name="myForm">
<input type="text" name="uname" placeholder="Username" maxlength="14"><br><br><br>
<input type="password" name="password" placeholder="password"><br><br><br>
<input type="submit" value="Submit" name="btn"><br><br><br>
<a href="register.php">New user?register here.</a>
</form>
</body>
</html>

<?php
error_reporting(0);
session_start();

if(isset($_POST['btn']))
{
$id=$_POST['uname'];
$pass=$_POST['password'];
try
{
    $dbh = new PDO('mysql:host=127.0.0.1;dbname=details', 'root', 'idkpass');
    $dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
}
catch(PDOException $ex){
	echo 'Execute Failed: '.$ex->getMessage();
}
$q = "SELECT username,password,cno,bank_name,amount FROM users WHERE username = :id and password= :pass";
$sth = $dbh->prepare($q);
$sth->bindParam(':id', $id);
$sth->bindParam(':pass',$pass);
$sth->execute();
$result = $sth->fetchAll();
if($result)
{
foreach($result as $row)
        {
		if ($row['username']!=='')
                        {
                                if ($row['password']!=='')
                                {
                                        $_SESSION['favcolor'] = $row['username'];
                                        $_SESSION['cnum'] = $row['cno'];
					$_SESSION['bkname'] = $row['bank_name'];
					$_SESSION['amont'] = $row['amount'];
                                        header("Location: dashboard.php");
                                }
                        }

        }
}
else
{
//A note from Admin of Bank Of CC : I have saved my credentials in a file , let's see if you can find it ;)
echo "<script>alert('umm...something bad happened')</script>";
}
}


?>
