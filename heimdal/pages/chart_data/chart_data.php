<?php
$_pairdata = new PairData($_mongo);
$asset_pair = $_pairdata->build_chart_object($_getset->header("pair_name"));

//print(json_encode($asset_pair['odin']['chart']));
?>
<script type="text/javascript">
cryptod_chart.update_labels(<?=json_encode($asset_pair['odin']['chart']['labels'])?>);
cryptod_chart.fill_dataset_simplified('Purchases', <?=json_encode($asset_pair['odin']['chart']['trades']['purchases'])?>);
cryptod_chart.fill_dataset_simplified('Sales', <?=json_encode($asset_pair['odin']['chart']['trades']['sales'])?>);
cryptod_chart.fill_dataset_simplified('P-Decision', <?=json_encode($asset_pair['odin']['chart']['decisions']['pdecision'])?>);
cryptod_chart.fill_dataset_simplified('S-Decision', <?=json_encode($asset_pair['odin']['chart']['decisions']['sdecision'])?>);
cryptod_chart.fill_dataset_simplified('P-Action', <?=json_encode($asset_pair['odin']['chart']['actions']['paction'])?>);
cryptod_chart.fill_dataset_simplified('S-Action', <?=json_encode($asset_pair['odin']['chart']['actions']['saction'])?>);

<?php foreach($asset_pair['odin']['chart']['analyses'] as $calculation=>$values) { ?>
cryptod_chart.fill_dataset_simplified('<?=$calculation?>', <?=json_encode($values)?>);
<?php } ?>

cryptod_chart.update();
</script>