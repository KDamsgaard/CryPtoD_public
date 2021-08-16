<?php
//$content['home'] = 'home';
$content['available'] = 'pair_data/available_pairs_tiles&init=1';
$content['watched'] = 'pair_data/watched_pairs_tiles&init=1&type=short';
//$content['split pairs'] = 'split_pairs';
//$content['watched pairs'] = 'watched_pairs';
$content['logs'] = 'logs';

$_template->print($content, 'menu');
?>