<?php
class Helpers {
    var $templates;
    function __construct($_templates) {
        $this->templates = $_templates;
    }

    function child_popup($title='', $icon='', $args=[]) {
        $content[$title]['icon'] = $icon;
        $content[$title]['args'] = $args;
        return $this->templates->load($content, 'hover_menu_popup');
    }

}
?>