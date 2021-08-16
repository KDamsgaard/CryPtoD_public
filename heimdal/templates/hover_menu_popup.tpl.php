<div class="popup_parent position_relative">
    <div class="popup_child hide rounded border border-dark">
    <?php
    if(isset($content)) {
        foreach($content as $key=>$item) {
            $link = "";
            foreach($item['args'] as $_key=>$_value) { $link .= $_key."=".$_value."&"; }
    ?>
        <div class="small m-1 p-0 text-dark">
            <?php if (isset($item['icon'])) { ?>
            <a class="p-0 m-0" href="?<?=$link?>">
                <img class="p-0 m-0" src="images/<?=$item['icon']?>" title="<?=$key?>">
            </a>
            <?php } else { ?>
                <img class="p-0 m-0" src="images/unknown-file.png" title="No icon for: <?=$key?>">
            <?php } ?>
        </div>
    <?php }} ?>
    </div>
    <div class="border rounded bg-dark p-0 m-0">
        <!-- <img src="images/menu.png"> -->
        M
    </div>
</div>