<?php foreach($content as $key=>$item) { ?>
  <div class="d-inline-flex pl-1 pr-1">
    <a class="text-decoration-none text-light font-weight-bold" href="?page=<?=$item?>"><?=strtoupper($key)?></a>
  </div>
<?php } ?>