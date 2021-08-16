<div class="p-0 m-0 w-100">
    <div class="m-0 p-0 d-inline mw-100">
        <?=$content['ws_name']?>
    </div>
    <?php if($content['watched']) { ?>
    <div class="m-0 p-0 d-inline bg-success w-25">
    W
    </div>
    <?php } else { ?>
    <div class="m-0 p-0 d-inline bg-danger w-25">
    N
    </div>
    <?php } ?>
</div>