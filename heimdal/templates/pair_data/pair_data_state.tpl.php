<?php
if ($content['odin']['watched']) {
    if ($content['odin']['wallet']['profit'] > 0) {
?>
        <div class="bg-success d-block w-100 m-0 p-0 flex-row border-bottom" style="height:4px;"></div>
    <?php } elseif ($content['odin']['wallet']['profit'] < 0) { ?>
        <div class="bg-danger d-block w-100 m-0 p-0 flex-row border-bottom" style="height:4px;"></div>
    <?php } else { ?>
        <div class="bg-color-gold d-block w-100 m-0 p-0 flex-row border-bottom" style="height:4px;"></div>
    <?php } ?>
<?php } else { ?>
        <div class="bg-color-dark-red d-block w-100 m-0 p-0 flex-row border-bottom" style="height:4px;"></div>
<?php } ?>