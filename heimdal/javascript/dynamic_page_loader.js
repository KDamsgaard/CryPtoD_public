let popup_interval;
let popup_timeout;
let _interval = {};

function _load(data) {
    return data;
}

function insert_html(target_id, content) {
    //content = content.replace('\\', '');
    jQuery('#'+target_id).html(content);
}

function load_page_interval(page, target_id, args, speed=3000, preload=false) {
    //console.log(args);
    //console.log('Loading content page='+page+'&'+args);
    if (preload) { jQuery('#'+target_id).load('endpoint.php?page='+page+'&'+args); }
    if (!(target_id in Object.keys(_interval))) {
        _interval[target_id] = '';
    }
    clearInterval(_interval[target_id]);
    _interval[target_id] = setInterval(function(){
                                console.log('Interval reloading content page='+page+'&'+args);
                                jQuery('#'+target_id).load('endpoint.php?page='+page+'&'+args);
                            }, speed);
}

function load_page_recursive(page, target_id, args='', speed=5000, callback=null) {
    setTimeout(function() {
        //console.log('Reload ' +target_id);
        jQuery.get('endpoint.php?page='+page+'&'+args, function(data) {
            data = _load(data);
            if (callback == null) { jQuery('#'+target_id).html(data); }
            else { callback(data); }
        }).done(function() {
            load_page_recursive(page, target_id, args, speed, callback);
        });
    },speed);
}

function load_page_reload(page, target_id, args, speed=500) {
    console.log(page+' - #' + target_id);
    clearInterval(_interval[target_id]);
    //jQuery('#'+target_id).load('endpoint.php?page='+page+'&'+args);
    setTimeout(function(){
        //console.log('Reloading content page='+page+'&'+args);
        jQuery.get('endpoint.php?page='+page+'&'+args, function(data) {
            jQuery('#'+target_id).html(data);
        });
    }, speed);
}

function load_page(page, target_id, args, speed=500) {
    console.log(page+' - #' + target_id);
    clearInterval(_interval[target_id]);
    //jQuery('#'+target_id).load('endpoint.php?page='+page+'&'+args);

    setTimeout(function() {
        jQuery.get('endpoint.php?page='+page+'&'+args, function(data) {
            jQuery('#'+target_id).html(data);
        });
    }, speed);
}

function popup(page, target_id, args) {
    jQuery('#'+target_id).html("");
    show_popup();
    load_page_interval(page, target_id, args, 5000, true);
}

function show_popup() {
    console.log("show_popup()");
    jQuery("#popup_parent").removeClass('hide');
    jQuery("#popup_parent").addClass('show');

    return false;
}

function hide_popup() {
    console.log("hide_popup()");
    jQuery('#popup_container').html("");
    jQuery("#popup_parent").removeClass('show');
    jQuery("#popup_parent").addClass('hide');
    clearInterval(popup_interval);
    clearTimeout(popup_timeout);

    document.location.reload();

    return false;
}

function toggle(id) {
    var classList = document.getElementById(id).classList;
    console.log("toggle");
    console.log(classList);
    for (var i=0; i<classList.length; i++) {
        if ('hide' == classList[i]) {
            console.log('found hide');
            jQuery('#'+id).removeClass('hide');
            jQuery('#'+id).addClass('show');
            break;
        }
        if ('show' == classList[i]) {
            console.log('found show');
            jQuery('#'+id).removeClass('show');
            jQuery('#'+id).addClass('hide');
            break;
        }
    }
}