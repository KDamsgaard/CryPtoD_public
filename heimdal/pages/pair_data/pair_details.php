<?php
define('TPL_PATH', 'pair_data');
if ($_getset->header("pair_name") != null) {
    $_pairdata = new PairData($_mongo);
    $asset_pair = $_pairdata->pair_info($_getset->header("pair_name"));

    if ($_getset->header("type") == 'short') {
        $content = array();
        $content['body'] = $_template->load($asset_pair, 'pair_data_state', null, TPL_PATH);
        $content['body'] .= $_template->load($asset_pair, 'pair_data_saerimner_short', null, TPL_PATH);
        $content['body'] .= $_template->load($asset_pair, 'pair_data_mimir_short', null, TPL_PATH);
        $content['body'] .= $_template->load($asset_pair, 'pair_data_odin_short', null, TPL_PATH);
        $_template->print($content, 'pair_data_short', TPL_PATH);
    }
    elseif ($_getset->header("type") == 'large') {
        $content = array();
        $content['state'] = $_template->load($asset_pair, 'pair_data_state', null, TPL_PATH);
        $content['odin'] = $_template->load($asset_pair, 'pair_data_odin', null, TPL_PATH);
        $content['mimir'] = $_template->load($asset_pair, 'pair_data_mimir', null, TPL_PATH);
        $content['saerimner'] = $_template->load($asset_pair, 'pair_data_saerimner', null, TPL_PATH);
        $content['pair'] = $_template->load($asset_pair, 'pair_data_pair', false, 'pair_data');
        $tpl = $_template->load($content, 'pair_data_large', null, 'pair_data');

        $menu =  $_helpers->child_popup('Chart', 'chart_icon.png', ['page'=>'chart_data/odin_chart','pair_name'=>$asset_pair['pair_name']]);
        $content = array();
        $content['head'] = $asset_pair['ws_name'];
        $content['body'] = $tpl;
        $content['menu'] = $menu;
        $_template->print_tile($content, 'medium_tall');
    }
    elseif ($_getset->header("type") == 'chart') {

    }
    else {
        print("pair_name = " . $_getset->header("pair_name") . " type = ".$_getset->header("type"));
    }
}
else {
    print("pair_name = " . $_getset->header("pair_name"));
}
?>