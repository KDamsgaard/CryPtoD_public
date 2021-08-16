<?php
$_pairdata = new PairData($_mongo);
$_pairdata->build_info_list();

$asset_pair = $_pairdata->get_pair_data($_getset->header("pair_name"));

$content['head'] = $_getset->header("pair_name");
//$content['body'] = $_template->load($asset_pair, 'pair_data');

$content['body'] = '';
$content['body'] = $_template->load($asset_pair, 'pair_data_state', false, 'pair_data');
$content['body'] .= $_template->load($asset_pair, 'pair_data_odin', false, 'pair_data');
$content['body'] .= $_template->load($asset_pair, 'pair_data_mimir', false, 'pair_data');
$content['body'] .= $_template->load($asset_pair, 'pair_data_saerimner', false, 'pair_data');
$content['body'] .= $_template->load($asset_pair, 'pair_data_pair', false, 'pair_data');
$content['body'] = $_template->load($content, 'pair_data_short', false, 'pair_data');
$content['pair_name'] = $asset_pair['pair_name'];
if ($_getset->header("tile") == 1) {
    $_template->print_tile($content, 'medium_tall');
}
else {
    print($content['body']);
}
?>