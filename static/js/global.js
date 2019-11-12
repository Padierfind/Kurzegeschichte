var loading_flag = false;

async function loop() {
    var s = '',
        p;

    p = Math.floor(((Math.sin(Date.now()/300)+1)/2) * 100);

    while (p >= 8) {
        s += '█';
        p -= 8;
    }
    s += ['⠀','▏','▎','▍','▌','▋','▊','▉'][p];

    location.hash = s;
    if(loading_flag == true){
        location.hash = "";
    }
    else{
        setTimeout(loop, 50);
    }
}


function toggleMenu(){
    $("#menu_expansion").toggle('slow');
}


function display_notification(notification_text){
    $("#notification").text(notification_text);
    $("#notification").slideDown("fast");

    setTimeout(function() {
        $("#notification").slideUp("fast");
    }, 3000);
}

function check_if_user_is_logged_in(){
        $.ajax({
        url: "/get_login_status"
        }).done(function (result) {
            if(result == "False"){
                return false;
            }
        $("#menu_expansion > li").toggleClass("hidden");
    });
}

$( document ).ready(function() {
    $("#menu_expansion").hide();

    var searchParams = new URLSearchParams(window.location.search)
    if(searchParams.has('notification')) {
        display_notification(searchParams.get('notification'));
    }

    check_if_user_is_logged_in();
});