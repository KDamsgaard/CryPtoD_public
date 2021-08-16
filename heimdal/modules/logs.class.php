<?php
class Logs {
    var $path;

    function __construct($path, $type='debug') {
        $this->path = $path.'/'.date('Y-m-d',time()).'_'.$type.'_log.txt';
    }

    function read_from_last_line($linecount=5) {
        $lines=array();
        $fp = fopen($this->path, "r");
        while(!feof($fp))
        {
           $line = fgets($fp, 4096);

           if (strlen($line) > 130) {
                $l = substr($line, 0, 130).'...';
           }
           else {
                $l = $line;
           }
           array_push($lines, $l);
           if (count($lines)>$linecount)
               array_shift($lines);
        }
        fclose($fp);
        return $lines;
    }
}
?>