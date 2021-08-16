<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.min.js" integrity="sha512-d9xgZrVZpmmQlfonhQUvTR7lMPtO7NkZMkA0ABN3PHCbKA5nqylQ/yWlFAyY6hYgdF1Qh6nYiuADWwKB4C2WSw==" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/moment@2.24.0"></script>
  	    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-moment@0.1.1"></script>
        <script src="https://cdn.jsdelivr.net/npm/hammerjs@2.0.8"></script>
        <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom@0.7.7"></script>

        <script src="javascript/dynamic_page_loader.js"></script>
        <script src="javascript/chart_colors.js"></script>
        <script src="javascript/cryptod_chart.js"></script>
        <script type="text/javascript">
            var cryptod_chart;
        </script>

        <link rel="stylesheet" href="styles/colors.css">
        <link rel="stylesheet" href="styles/heimdal.css">
        <link rel="stylesheet" href="styles/tiles.css">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">

    </head>
    <body class="position_relative" style="background-color:#e8e7e3;">
        <div id="popup_parent" class="popup_parent zindex-popup hide position_relative w-100 h-100 popup_parent_background border" onclick="hide_popup();">
            <div id="popup_container" class="popup_container"></div>
        </div>
        <div class="bg-dark w-100 p-1 text-light align_top zindex-menu">
            <div class="d-inline-flex">
            <?php
                require_once 'pages/menu.php';
            ?>
            </div>
            <!-- Search field -->
            <!-- TODO fix size and position
            <div class="w-25 d-inline-flex">
                <form method="get" action="?">
                    <input class="w-100 form-control no-border text-center flex-column small" type="text" name="search" value="<?=$_getset->header("search")?>" placeholder="Search for asset pair">
                </form>
            </div>
            -->
        </div>
        <div id="body_container" class="align_top pt-5 pb-5 pl-2 pr-2 w-100 justify-content-center d-flex zindex-body flex-wrap">
            <?php
                if ($_getset->header("authorized") == 1) {
                    require_once 'pages/' . $_getset->header("page") . '.php';
                }
                else {
                    require_once 'pages/login.php';
                }
            ?>
        </div>

        <!-- This is used to load collective pair data with dynamic loaded js -->
        <div class="hide" id="script_async" type="text/javascript"></div>
    </body>
</html>
