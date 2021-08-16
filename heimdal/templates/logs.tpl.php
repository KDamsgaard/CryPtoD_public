<div class="overflow-auto text-left" style="font-size:0.7em;height:95%;">
<?php foreach($content as $line) { ?>

    <?php if (strstr($line, 'INFO')) { ?>
        <div class="text-dark bg-light w-100 border-bottom"><?=$line?></div>
    <?php } ?>

    <?php if (strstr($line, 'WARNING')) { ?>
        <div class="bg-warning w-100 border-bottom"><?=$line?></div>
    <?php } ?>

    <?php if (strstr($line, 'ERROR')) { ?>
        <div class="bg-danger w-100 border-bottom"><?=$line?></div>
    <?php } ?>

    <?php if (strstr($line, 'DEBUG')) { ?>
        <div class="bg-info w-100 border-bottom"><?=$line?></div>
    <?php } ?>

<?php } ?>
</div>
<!-- <textarea style="font-size:0.6em;height:95%;" class="w-100"><?=$content?></textarea> -->