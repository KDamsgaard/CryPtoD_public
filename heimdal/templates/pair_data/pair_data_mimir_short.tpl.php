<div class="d-flex ml-1 mr-1 border-bottom">
    <div class="p-0 m-0 w-50 small flex-column text-left">
        Score:
    </div>
    <div class="p-0 m-0 w-50 small flex-column text-right">
        <?php if (!empty($content['mimir']['scores']['ultimate'])) { ?>
            <?=round($content['mimir']['scores']['ultimate']['scores']['original'],4)?>
        <?php } ?>
    </div>
</div>
<div class="d-flex ml-1 mr-1 border-bottom">
    <div class="p-0 m-0 w-50 small flex-column text-left">
        De Score:
    </div>
    <div class="p-0 m-0 w-50 small flex-column text-right">
        <?php if (!empty($content['mimir']['scores']['ultimate'])) { ?>
            <?=round($content['mimir']['scores']['ultimate']['scores']['degenerated'],4)?>
        <?php } ?>
    </div>
</div>