<?php
class TemplateLoader {
    var $tpl_base_dir;
    var $dynamic_helper_tpl;

    function __construct($tpl_base_dir) {
        $this->tpl_base_dir = $tpl_base_dir;
        $this->dynamic_helper_tpl = 'helper_dynamic_loading';
    }

    private function trim_html($tpl) {
        $tpl = str_replace('"', '\"', $tpl);
        $tpl = str_replace("'", "\'", $tpl);
        $tpl = str_replace("\n", "", $tpl);
        $tpl = str_replace("\r", "", $tpl);
        return $tpl;
    }

    function tile($content=array(), $template='', $trim=false, $path='sys_tiles') {
        // Build path to template file
        $_template = $this->tpl_base_dir.'/'.$path.'/tile_'.$template.'.tpl.php';

        // Start buffer
        ob_start();
        // require template into buffer
        require $_template;
        // Get buffer contents
        $_template = ob_get_contents();
        ob_end_clean();

        if ($trim) { $_template = $this->trim_html(''.$_template); }

        return $_template;
    }

    function load($content=array(), $template='', $trim=false, $path=null) {
        // Build path to template file
        if ($path != null) { $_template = $this->tpl_base_dir.'/'.$path.'/'.$template.'.tpl.php'; }
        else { $_template = $this->tpl_base_dir.'/'.$template.'.tpl.php'; }

        // Start buffer
        ob_start();
        // require template into buffer
        require $_template;
        // Get buffer contents
        $_template = ob_get_contents();
        ob_end_clean();

        if ($trim) { $_template = $this->trim_html(''.$_template); }

        return $_template;
    }

    function print($content=array(), $template='', $path=null) {
        $tpl = $this->load($content, $template, false, $path);
        print($tpl);
        return $tpl;
    }

    function print_tile($content=array(), $template='', $path='sys_tiles') {
        if ($path != null) {
            $tpl = $this->tile($content, $template, false, $path);
            print($tpl);
            return $tpl;
        }
        else {
            $tpl = $this->tile($content, $template);
            print($tpl);
            return $tpl;
        }
    }

}
?>