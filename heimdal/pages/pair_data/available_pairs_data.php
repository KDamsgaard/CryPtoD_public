<?php
$_pairdata = new PairData($_mongo);
$_pairdata->build_info_list();
?>

<script type="text/javascript">
<?php
/** Section for available pairs data **/
// Go through all pairs to find what to display
foreach($_pairdata->pairdata['available'] as $asset_pair) {
    if ($asset_pair['saerimner']['trades']['info']['trades'] > 0) {
        $tpl = $_template->load($asset_pair, 'pair_data_short', true);
?>
    insert_html("<?=$asset_pair['pair_name']?>", "<?=$tpl?>");
<?php }} ?>

load_page('pair_data/available_pairs_data', 'script_async', '', 3000);
</script>