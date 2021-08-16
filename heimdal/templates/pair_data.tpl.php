<div class="d-flex p-0 m-0">
    <div class="flex-row w-100 p-0 m-0">

         <?php if ($content['odin']['watched']) { ?>
            <?php if ($content['odin']['wallet']['profit'] > 0) { ?>
                <div class="bg-success d-block w-100 m-0 p-0 flex-row border-bottom" style="height:4px;"></div>
            <?php } elseif ($content['odin']['wallet']['profit'] < 0) { ?>
                <div class="bg-danger d-block w-100 m-0 p-0 flex-row border-bottom" style="height:4px;"></div>
            <?php } else { ?>
                <div class="bg-color-gold d-block w-100 m-0 p-0 flex-row border-bottom" style="height:4px;"></div>
            <?php } ?>
        <?php } else { ?>
            <div class="bg-color-dark-red d-block w-100 m-0 p-0 flex-row border-bottom" style="height:4px;"></div>
        <?php } ?>

        <div class="w-100 text-dark font-weight-bold small mt-1 border-bottom">
            Saerimner
        </div>
        <div class="d-flex ml-1 mr-1 border-bottom">
            <div class="p-0 m-0 w-50 small flex-column text-left">
                Trades:
            </div>
            <div class="p-0 m-0 w-50 small flex-column text-right">
                <?=$content['saerimner']['trades']['info']['trades']?>
            </div>
        </div>
        <div class="d-flex ml-1 mr-1 border-bottom">
            <div class="p-0 m-0 w-50 small flex-column text-left">
                Trades/h:
            </div>
            <div class="p-0 m-0 w-50 small flex-column text-right">
                <?=$content['saerimner']['trades']['info']['trades_hour']?>
            </div>
        </div>
        <div class="d-flex ml-1 mr-1 border-bottom">
            <div class="p-0 m-0 w-50 small flex-column text-left">
                Timespan:
            </div>
            <div class="p-0 m-0 w-50 small flex-column text-right">
                <?=$content['saerimner']['trades']['info']['trades_hour_span']?>
            </div>
        </div>

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
            <div class="p-0 m-0 w-50 small flex-column text-left">
            </div>
            <div class="p-0 m-0 w-50 small flex-column text-right">
                <?php foreach($content['mimir']['scores']['ultimate']['factors'][$key]['constraints'] as $constraint) { ?>
                    (<?=$key?> <?=$constraint['operator']?> <?=$constraint['target']?>)
                <?php } ?>
            </div>
        </div>
        <?php } ?>

        <div class="w-100 text-dark font-weight-bold small mt-1 border-bottom">
            Odin
        </div>
        <div class="d-flex ml-1 mr-1 border-bottom">
            <div class="p-0 m-0 w-50 small flex-column text-left">
                Profit:
            </div>
            <div class="p-0 m-0 w-50 small flex-column text-right">
                <?=round($content['odin']['wallet']['profit'],4)?>
            </div>
        </div>
        <div class="d-flex ml-1 mr-1 border-bottom">
            <div class="p-0 m-0 w-50 small flex-column text-left">
                Purse:
            </div>
            <div class="p-0 m-0 w-50 small flex-column text-right">
                <?=$content['odin']['wallet']['purse']?>
            </div>
        </div>
        <div class="d-flex ml-1 mr-1 border-bottom">
            <div class="p-0 m-0 w-50 small flex-column text-left">
                Coins:
            </div>
            <div class="p-0 m-0 w-50 small flex-column text-right">
                <?=$content['odin']['wallet']['coins']?>
            </div>
        </div>
        <div class="d-flex ml-1 mr-1 border-bottom">
            <div class="p-0 m-0 w-50 small flex-column text-left">
                Trades:
            </div>
            <div class="p-0 m-0 w-50 small flex-column text-right">
                <?=$content['odin']['trades']['info']['trades']?>
            </div>
        </div>
        <div class="d-flex ml-1 mr-1 border-bottom">
            <div class="p-0 m-0 w-50 small flex-column text-left">
                Trades/h:
            </div>
            <div class="p-0 m-0 w-50 small flex-column text-right">
                <?=$content['odin']['trades']['info']['trades_hour']?>
            </div>
        </div>
        <div class="d-flex ml-1 mr-1 border-bottom">
            <div class="p-0 m-0 w-50 small flex-column text-left">
                Trades timespan:
            </div>
            <div class="p-0 m-0 w-50 small flex-column text-right">
                <?=$content['odin']['trades']['info']['trades_hour_span']?>
            </div>
        </div>
        <div class="d-flex ml-1 mr-1 border-bottom">
            <div class="p-0 m-0 w-50 small flex-column text-left">
                Analyses:
            </div>
            <div class="p-0 m-0 w-50 small flex-column text-right">
                <?=$content['odin']['analyses']['info']['analyses']?>
            </div>
        </div>
        <div class="d-flex ml-1 mr-1 border-bottom">
            <div class="p-0 m-0 w-50 small flex-column text-left">
                Analyses/h:
            </div>
            <div class="p-0 m-0 w-50 small flex-column text-right">
                <?=$content['odin']['analyses']['info']['analyses_hour']?>
            </div>
        </div>
        <div class="d-flex ml-1 mr-1 border-bottom">
            <div class="p-0 m-0 w-50 small flex-column text-left">
                Analyses timespan:
            </div>
            <div class="p-0 m-0 w-50 small flex-column text-right">
                <?=$content['odin']['analyses']['info']['analyses_hour_span']?>
            </div>
        </div>
    </div>
</div>