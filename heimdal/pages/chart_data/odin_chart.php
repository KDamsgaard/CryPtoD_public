<?php
//$_getset->setStandardValue("pair_name", "XXBTZEUR");
//$_getset->setSession('pair_name', $_getset->header("pair_name"));
$_pairdata = new PairData($_mongo);
$asset_pair = $_pairdata->build_chart_object($_getset->header("pair_name"));

//$_toolbox->pprint($asset_pair);
define('TPL_PATH', 'pair_data');
?>

<div class="d-flex w-100">
    <div id="chart" class="flex-column w-75 text-center">
        <?php
          $content['head'] = $asset_pair['ws_name'];
          $content['body'] = $_template->load($asset_pair, 'chart');
          $_template->print_tile($content, 'full_width');
        ?>
    </div>
    <div class="flex-column w-25 text-center">
        <?php
        $content = array();
        $content['body'] = $_template->load($asset_pair, 'pair_data_state', null, TPL_PATH);
        $content['body'] .= $_template->load($asset_pair, 'pair_data_odin', null, TPL_PATH);
        $content['body'] .= $_template->load($asset_pair, 'pair_data_mimir', null, TPL_PATH);
        $content['body'] .= $_template->load($asset_pair, 'pair_data_saerimner', null, TPL_PATH);
        $content['body'] .= $_template->load($asset_pair, 'pair_data_pair', null, TPL_PATH);
        $content['pair_name'] = $asset_pair['pair_name'];
        $tpl = $_template->load($content, 'pair_data_short', false, 'pair_data');

        $content = array();
        $content['head'] = $asset_pair['ws_name'];
        //$content['body'] = $_template->load($asset_pair, 'pair_data', null, 'pair_data');
        $content['body'] = $tpl;
        $content['id'] = 'pair_data';
        $_template->print_tile($content, 'medium_tall');
        ?>
    </div>
</div>


<script type="text/javascript">
    load_page_recursive('chart_data/chart_data', 'script_async', 'pair_name=<?=$_getset->header("pair_name")?>', 1000);
    load_page_recursive('pair_data/pair_data', 'pair_data', 'pair_name=<?=$_getset->header("pair_name")?>&tile=0', 5000);
</script>
