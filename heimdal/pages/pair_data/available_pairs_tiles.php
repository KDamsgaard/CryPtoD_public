<?php
$_pairdata = new PairData($_mongo);
$_pairdata->build_info_list();
define('TPL_PATH', 'pair_data');
?>

<?php
/** Section for available pairs data **/
// Go through all pairs to find what to display
foreach($_pairdata->pairdata['available'] as $asset_pair) {
    if ($asset_pair['saerimner']['trades']['info']['trades'] >= 1) {
        $content = array();
        $content['body'] = $_template->load($asset_pair, 'pair_data_state', null, TPL_PATH);
        $content['body'] .= $_template->load($asset_pair, 'pair_data_saerimner_short', null, TPL_PATH);
        $content['body'] .= $_template->load($asset_pair, 'pair_data_mimir_short', null, TPL_PATH);
        $content['body'] .= $_template->load($asset_pair, 'pair_data_odin_short', null, TPL_PATH);
        $content['pair_name'] = $asset_pair['pair_name'];


        $content['head'] = $asset_pair['ws_name'];
        $content['menu'] = $_helpers->child_popup('Chart', 'chart_icon.png', ['page'=>'chart_data/odin_chart','pair_name'=>$asset_pair['pair_name']]);
        $content['id'] = $asset_pair['pair_name'];
        $content['body'] = $_template->load($content, 'pair_data_short', null, 'pair_data');

        $_template->print_tile($content, 'small');
    }
}
?>
<script type="text/javascript">
//     load_page_recursive('pair_data/available_pairs_data', 'script_async', args='', speed=5000);
//     load_page_recursive('pair_data/available_pairs_tiles', 'body_container', args='', speed=10000);
</script>
<script type="text/javascript">
    load_page_reload('pair_data/available_pairs_tiles', 'body_container', '', 15000);

    <?php if ($_getset->header("init") == 1) { ?>
        load_page('pair_data/available_pairs_data', 'script_async', '');
    <?php } ?>
</script>
