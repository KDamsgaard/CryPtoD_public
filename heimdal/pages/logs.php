<?php
$_getset->setSession("subsystem", $_getset->header("subsystem"));
$_getset->setSession("type", $_getset->header("type"));

$subsystems[] = '<a class="btn btn-secondary m-0 mt-1 mb-1 p-0 w-100" href="?subsystem=mimir">Mimir</a><br>';
$subsystems[] = '<a class="btn btn-secondary m-0 mt-1 mb-1 p-0 w-100" href="?subsystem=odin">Odin</a><br>';
$subsystems[] = '<a class="btn btn-secondary m-0 mt-1 mb-1 p-0 w-100" href="?subsystem=saerimner">Sarimner</a><br>';

$type[] = '<a class="btn btn-secondary m-0 mt-1 mb-1 p-0 w-100" href="?type=debug">Debug</a><br>';
$type[] = '<a class="btn btn-secondary m-0 mt-1 mb-1 p-0 w-100" href="?type=error">Error</a><br>';


$content['head'] = 'Subsystem';
$content['body'] = implode($subsystems);
$_template->print($content, 'tile_small');

$content['head'] = 'Type';
$content['body'] = implode($type);
$_template->print($content, 'tile_small');

if ($_getset->header("subsystem") != null & $_getset->header("type") != null) {
    $_logs = new Logs('../'.$_getset->header('subsystem').'/logs/', $_getset->header('type'));

    $content['head'] = 'Logs - '.$_getset->header("subsystem").' - '.$_getset->header("type");
    $content['body'] = $_template->load($_logs->read_from_last_line(30),'logs');
    $_template->print($content, 'tile_large');
}
?>

<script type="text/javascript">
    load_page_reload('logs', 'body_container', '');
</script>
