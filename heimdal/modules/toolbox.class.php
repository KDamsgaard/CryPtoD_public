<?php
/*
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Søren B. Ølholm
*/
class Toolbox {
    function __construct() {
    }

    function pprint($array) {
        print("<pre>");
        print_r($array);
        print("</pre");
    }

    function format_timestamp($time) {
        return date('Y-m-d H:m:i', $time);
    }

    function jsconsole($message) {
        $js = '<script type="text/javascript">
                console.log("'.$message.'");
               </script>';
        print($js);
    }

    function page_reload($page, $container, $args, $speed=3000) {
        $js = "<script type=\"text/javascript\">
                load_page_reload('".$page."', '".$container."', '".$args."', ".$speed.");
               </script>";
        print($js);
    }
}
?>