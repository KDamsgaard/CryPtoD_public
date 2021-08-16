<?php
$login_tpl = $_template->load([], 'login');

$content['head'] = 'Please login in';
$content['body'] = $login_tpl;

$_template->print_tile($content, 'medium');
?>