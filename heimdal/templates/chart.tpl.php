<div class="border" style="width:100%; height:800px;">
    <canvas id="cryptod_chart" style="height:100%; width:100%;"></canvas>
</div>

<script type="text/javascript">
cryptod_chart = new CryPtoD_Chart('cryptod_chart', chart_colors, 10000);

cryptod_chart.add_dataset('Purchases', 'trades_purchases',{pointStyle: 'rect',radius: 2,showLine: false});
cryptod_chart.add_dataset('Sales', 'trades_sales',{pointStyle: 'rect',radius: 2,showLine: false});
cryptod_chart.add_dataset('P-Decision', 'decisions_purchases',{pointStyle: 'triangle', pointRadius: 10, borderWidth: 2});
cryptod_chart.add_dataset('S-Decision', 'decisions_sales',{pointStyle: 'triangle', pointRadius: 10, pointRotation: 180, borderWidth: 2});
cryptod_chart.add_dataset('P-Action', 'actions_purchases',{pointStyle: 'triangle', pointRadius: 30, borderWidth: 2});
cryptod_chart.add_dataset('S-Action', 'actions_sales',{pointStyle: 'triangle', pointRadius: 30, pointRotation: 180, borderWidth: 2});

<?php foreach($content['odin']['chart']['analyses'] as $calculation=>$values) { ?>
cryptod_chart.add_dataset('<?=$calculation?>', '<?=$calculation?>', {pointRadius: 0, borderWidth: 1,showLine: true});
<?php } ?>

cryptod_chart.update_labels(<?=json_encode($content['odin']['chart']['labels'])?>);
cryptod_chart.fill_dataset_simplified('Purchases', <?=json_encode($content['odin']['chart']['trades']['purchases'])?>);
cryptod_chart.fill_dataset_simplified('Sales', <?=json_encode($content['odin']['chart']['trades']['sales'])?>);
cryptod_chart.fill_dataset_simplified('P-Decision', <?=json_encode($content['odin']['chart']['decisions']['pdecision'])?>);
cryptod_chart.fill_dataset_simplified('S-Decision', <?=json_encode($content['odin']['chart']['decisions']['sdecision'])?>);
cryptod_chart.fill_dataset_simplified('P-Action', <?=json_encode($content['odin']['chart']['actions']['paction'])?>);
cryptod_chart.fill_dataset_simplified('S-Action', <?=json_encode($content['odin']['chart']['actions']['saction'])?>);

<?php foreach($content['odin']['chart']['analyses'] as $calculation=>$values) { ?>
cryptod_chart.fill_dataset_simplified('<?=$calculation?>', <?=json_encode($values)?>);
<?php } ?>

cryptod_chart.update();
</script>

<div id="chart_data"></div>
<script type="text/javascript">
    //load_page_interval('chart_data', 'chart_data', 'pair_name=<?=$content["pair_name"]?>', 5000);
</script>