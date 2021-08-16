<?php
session_start();

// Include modules
require_once 'modules/settings.php';
require_once 'modules/getset.php';
require_once 'modules/vendor/autoload.php';
require_once 'modules/MongoDB.class.php';
require_once 'modules/toolbox.class.php';
require_once 'modules/template_loader.class.php';
require_once 'modules/helpers.class.php';

require_once 'modules/saerimner.class.php';
require_once 'modules/mimir.class.php';
require_once 'modules/odin.class.php';
require_once 'modules/pairdata.class.php';

require_once 'modules/logs.class.php';

// Initialize modules
$_getset = new GetSet();
$_toolbox = new Toolbox();
$_mongo = new MongoDB('localhost', '27017');
$_template = new TemplateLoader('templates');
$_helpers = new Helpers($_template);

//$_getset->setStandardValue('page', 'home');
//$_getset->setSession('page', $_getset->header("page"));

require_once 'pages/' . $_getset->header("page") . '.php';
?>