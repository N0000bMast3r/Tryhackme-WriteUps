<?php
$secret = hash_hmac('sha256', 'hacker.com', false);
print($secret)
?>