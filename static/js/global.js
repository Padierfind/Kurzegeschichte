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
                return;
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