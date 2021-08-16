<?php
$_pairdata = new PairData($_mongo);
$_pairdata->build_info_list();
define('TPL_PATH', 'pair_data');
?>

<script type="text/javascript">
<?php
/** Section for available pairs data **/
// Go through all pairs to find what to display
foreach($_pairdata->pairdata['watched'] as $asset_pair) {
    $content = array();
    $content['body'] = $_template->load($asset_pair, 'pair_data_state', null, TPL_PATH);
    $content['body'] .= $_template->load($asset_pair, 'pair_data_saerimner_short', null, TPL_PATH);
    $content['body'] .= $_template->load($asset_pair, 'pair_data_mimir_short', null, TPL_PATH);
    $content['body'] .= $_template->load($asset_pair, 'pair_data_odin_short', null, TPL_PATH);
    $content['pair_name'] = $asset_pair['pair_name'];
    //$_template->print($content, 'pair_data_short', TPL_PATH);
    $tpl = $_template->load($content, 'pair_data_short', true, 'pair_data');
    //print("insert_html(\"".$asset_pair['pair_name']."\", \"".$tpl."\");\n");
?>
    insert_html("<?=$asset_pair['pair_name']?>", "<?=$tpl?>");
<?php } ?>

load_page('pair_data/watched_pairs_data', 'script_async', '', 3000);
</script>