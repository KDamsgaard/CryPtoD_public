<?php
if (isset($content['menu'])) { $menu = $content['menu']; }
else { $menu = ''; }

if (isset($content['head'])) { $head = $content['head']; }
else { $head = ''; }

if (isset($content['body'])) { $body = $content['body']; }
else { $body = ''; }

if (isset($content['id'])) { $body_id = $content['id']; }
else { $body_id = ''; }
?>

<div class="d-inline-flex bg-light border border-secondary tile tile_full_width text-center rounded">
    <div class="flex-row w-100">
        <div class="pl-1 pr-1 text-light bg-dark w-100">
            <table class="p-0 m-0 w-100 text-center text-light popup_parent position_relative">
                <tr>
                    <td class="">
                        <?=$content['head']?>
                    </td>
                    <td class="popup_parent position_relative" style="width:30px;">
                        <?php if (isset($content['menu'])) { ?>
                        <?=$content['menu']?>
                        <?php } ?>
                    </td>
                </tr>
            </table>
        </div>
        <div id="<?=$body_id?>" class="pl-0 pr-0 h-auto">
            <?=$content['body']?>
        </div>
    </div>
</div>