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