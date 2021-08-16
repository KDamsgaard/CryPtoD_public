<?php
if (isset($content['menu'])) { $menu = $content['menu']; }
else { $menu = ''; }

if (isset($content['head'])) { $head = $content['head']; }
else { $head = ''; }

if (isset($content['body'])) { $body = $content['body']; }
else { $body = ''; }

if (isset($content['id'])) { $body_id = $content['id']; }
else { $body_id = ''; }

if (isset($content['page'])) { $body_page = $content['page']; }
else { $body_page = ''; }

if (isset($content['args'])) { $body_args = $content['args']; }
else { $body_args = ''; }

if (isset($content['reload'])) { $body_reload = $content['reload']; }
else { $body_reload = ''; }
?>

<div class="d-inline-flex bg-color-lightest border border-secondary tile tile_small text-center rounded">
    <div class="flex-row w-100">
        <div class="pl-0 pr-0 text-light bg-dark w-100">
            <table class="p-0 m-0 w-100 text-center text-light popup_parent position_relative">
                <tr>
                    <td class="">
                        <?=$head?>
                    </td>
                    <td class="popup_parent position_relative" style="width:30px;">
                        <?=$menu?>
                    </td>
                </tr>
            </table>
        </div>
        <div id="<?=$body_id?>" class="pl-0 pr-0 h-auto">
            <?=$body?>
        </div>
    </div>
</div>

<?php if ($body_id != '' && $body_page != '') { ?>
<script type="text/javascript">
//load_page_recursive(page, target_id, args, speed);
load_page_recursive('<?=$body_page?>', '<?=$body_id?>', '<?=$body_args?>', <?=$body_reload?>);
</script>
<?php } ?>