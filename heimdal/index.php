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
$_pairdata = new PairData($_mongo);
$_helpers = new Helpers($_template);

$_getset->setStandardValue('page', 'available_pairs');
$_getset->setSession('page', $_getset->header("page"));

/*************** LOGIN **************/
// Check for user login
if ($_getset->header("action") == 'login') {
    $_toolbox->jsconsole("login");
    // Check for correct username and password
    if ($_getset->header("username") == ADMIN_USERNAME && $_getset->header("password") == ADMIN_PASSWORD) {
        $_toolbox->jsconsole("ok");
        // Set user as authorized
        $_getset->setSession('authorized', 1);
    }
    else {
        $_toolbox->jsconsole("Not ok");
        // Set user as unauthorized
        $_getset->setSession('authorized', 0);
        // Destroy session
        session_destroy();
    }
}
else {
    $_toolbox->jsconsole("no login");
}

// Check for user logout
if ($_getset->header("action") == 'logout') {
    // Set user as unauthorized
    $_getset->setSession('authorized', 0);
    // Destroy session
    session_destroy();
}
/*************** END LOGIN **************/


/************** Layout & Content *****************/


require_once 'templates/body.tpl.php';


/************** END Layout & Content *****************/
?>