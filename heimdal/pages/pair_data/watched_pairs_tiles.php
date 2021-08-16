<?php
$_pairdata = new PairData($_mongo);
$_pairdata->build_info_list();
define('TPL_PATH', 'pair_data');
?>

<?php
/** Section for available pairs data **/
// Go through all pairs to find what to display
foreach($_pairdata->pairdata['watched'] as $asset_pair) {
    $content = array();
    $content['body'] = $_template->load($asset_pair, 'pair_data_state', null, TPL_PATH);
    $content['body'] .= $_template->load($asset_pair, 'pair_data_saerimner_short', null, TPL_PATH);
    $content['body'] .= $_template->load($asset_pair, 'pair_data_mimir_short', null, TPL_PATH);
    $content['body'] .= $_template->load($asset_pair, 'pair_data_odin_short', null, TPL_PATH);
    $tpl = $_template->load($content, 'pair_data_short', null, TPL_PATH);

    $content = array();
    $menu =  $_helpers->child_popup('Chart', 'chart_icon.png', ['page'=>'chart_data/odin_chart','pair_name'=>$asset_pair['pair_name']]);
    $content['head'] = $asset_pair['ws_name'];
    $content['id'] = $asset_pair['pair_name'];
    $content['menu'] = $menu;
    $content['body'] = $tpl;
    $_template->print_tile($content, 'small');
}
?>
<script type="text/javascript">
    load_page_reload('pair_data/watched_pairs_tiles', 'body_container', '', 15000);

    <?php if ($_getset->header("init") == 1) { ?>
        load_page('pair_data/watched_pairs_data', 'script_async', '');
    <?php } ?>
</script>