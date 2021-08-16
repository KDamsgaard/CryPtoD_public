<?php
$_pairdata = new PairData($_mongo);
$_pairdata->build_info_list();


?>

<div class="w-100 text-center rounded mb-1 border">
    <div class="w-100 bg-dark text-center text-light rounded">
        <b>Watched</b> - <?=count($_pairdata->pairdata['watched'])?>
    </div>
    <div id="watched_pairs" class="m-0 p-0 w-100 h-100">
    <?php
    /** Section for available pairs data **/
    // Go through all pairs to find what to display
    foreach($_pairdata->pairdata['watched'] as $asset_pair) {
        $content['head'] = $asset_pair['ws_name'];
        $content['menu'] = $_helpers->child_popup('Chart', 'chart_icon.png', ['page'=>'odin_chart','pair_name'=>$asset_pair['pair_name']]);
        $content['body'] = $_template->load($asset_pair, 'pair_data_short');
        $content['id'] = $asset_pair['pair_name'];
        $_template->print_tile($content, 'small');
    }
    ?>
    </div>
</div>


<div class="w-100 text-center rounded mb-1 border">
    <div class="w-100 bg-dark text-center text-light rounded" onclick="toggle('available_pairs');">
        <b>Available</b> - <?=count($_pairdata->pairdata['available'])?>
    </div>
    <div id="available_pairs" class="w-100 h-100 m-0 p-0 hide">
    <?php
    /** Section for available pairs data **/
    // Go through all pairs to find what to display
    foreach($_pairdata->pairdata['available'] as $asset_pair) {
        $content['head'] = $asset_pair['ws_name'];
        $content['menu'] = $_helpers->child_popup('Chart', 'chart_icon.png', ['page'=>'odin_chart','pair_name'=>$asset_pair['pair_name']]);
        $content['body'] = $_template->load($asset_pair, 'pair_data_short');
        $content['id'] = $asset_pair['pair_name'];
        $_template->print_tile($content, 'small');
    }
    ?>
    </div>
</div>

<script type="text/javascript">
    load_page_recursive('pair_data/watched_pairs_data', 'script_async');
    load_page_recursive('pair_data/available_pairs_data', 'script_async', '', 30000);
    load_page_recursive('pair_data/watched_pairs_tiles', 'watched_pairs', '', 10000);
    load_page_recursive('pair_data/available_pairs_tiles', 'available_pairs', '', 10000);
</script>