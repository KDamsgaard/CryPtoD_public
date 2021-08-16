 <div class="w-100 text-dark font-weight-bold small mt-1 border-bottom">
    Mimir
</div>
<div class="d-flex ml-1 mr-1 border-bottom">
    <div class="p-0 m-0 w-50 small flex-column text-left">
        Analyzer:
    </div>
    <div class="p-0 m-0 w-50 small flex-column text-right">
        <?=$content['mimir']['scores']['ultimate']['analyzer']?>
    </div>
</div>
<div class="d-flex ml-1 mr-1 border-bottom">
    <div class="p-0 m-0 w-50 small flex-column text-left">
        Score:
    </div>
    <div class="p-0 m-0 w-50 small flex-column text-right">
        <?=$content['mimir']['scores']['ultimate']['scores']['original']?>
    </div>
</div>
<div class="d-flex ml-1 mr-1 border-bottom">
    <div class="p-0 m-0 w-50 small flex-column text-left">
        De Score:
    </div>
    <div class="p-0 m-0 w-50 small flex-column text-right">
        <?=$content['mimir']['scores']['ultimate']['scores']['degenerated']?>
    </div>
</div>
<?php foreach(array_keys($content['mimir']['scores']['ultimate']['factors']) as $key) { ?>
<div class="d-flex ml-1 mr-1 border-bottom">
    <div class="p-0 m-0 w-50 small flex-column text-left">
        <?=$key?>:
    </div>
    <div class="p-0 m-0 w-50 small flex-column text-right">
        <?=$content['mimir']['scores']['ultimate']['factors'][$key]['value']?>
    </div>
</div>
<div class="d-flex ml-1 mr-1 border-bottom">
    <div class="p-0 m-0 w-100 small flex-column text-right">
        <?php foreach($content['mimir']['scores']['ultimate']['factors'][$key]['constraints'] as $constraint) { ?>
            <?=$key?> <?=$constraint['operator']?> <?=$constraint['target']?>
        <?php } ?>
    </div>
</div>
<?php } ?>