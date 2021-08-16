<div class="d-flex p-0 m-0 bg-color-lightest"  onclick="popup('pair_data/pair_details', 'popup_container', 'pair_name=<?=$content['pair_name']?>&type=large&tile=1');">
    <div class="flex-row w-100 p-0 m-0">
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
        <!--
        <div class="d-flex ml-1 mr-1 border-bottom">
            <div class="p-0 m-0 w-50 small flex-column text-left">
                Timespan:
            </div>
            <div class="p-0 m-0 w-50 small flex-column text-right">
                <?=$content['saerimner']['trades']['info']['trades_hour_span']?>
            </div>
        </div>
        -->

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
                Coins:
            </div>
            <div class="p-0 m-0 w-50 small flex-column text-right">
                <?=round($content['odin']['wallet']['coins'], 4)?>
            </div>
        </div>
        <!--
        <div class="d-flex ml-1 mr-1 border-bottom">
            <div class="p-0 m-0 w-50 small flex-column text-left">
                Purse:
            </div>
            <div class="p-0 m-0 w-50 small flex-column text-right">
                <?=round($content['odin']['wallet']['purse'],4)?>
            </div>
        </div>
        -->
    </div>
</div>
<!-- </a> -->