<?php
$_pairdata = new PairData($_mongo);
$_pairdata->build_info_list();
?>

<div class="w-100 text-center rounded mb-1 border">
    <div class="w-100 bg-dark text-center text-light rounded">
        <b>Watched</b> - <?=count($_pairdata->pairdata['watched'])?>
    </div>
    <?php
    /** Section for available pairs data **/
    // Go through all pairs to find what to display
    foreach($_pairdata->pairdata['watched'] as $asset_pair) {
        $content['head'] = $asset_pair['ws_name'];
        $content['menu'] = $_helpers->child_popup('Chart', 'chart_icon.png', ['page'=>'odin_chart','pair_name'=>$asset_pair['pair_name']]);
        $content['body'] = $_template->load($asset_pair, 'available_pair_names');
        //$content['page'] = 'pair_details';
        $content['id'] = $asset_pair['pair_name'];
        //$content['args'] = 'pair_name='.$asset_pair['pair_name'].'&type=short';
        //$content['reload'] = 5000;
        $_template->print_tile($content, 'small');
    }
    ?>
</div>

<script type="text/javascript">
    load_page_recursive('available_pairs_data', 'script_async');
    load_page_recursive('available_pairs', 'body_container', '', 30000);
</script>