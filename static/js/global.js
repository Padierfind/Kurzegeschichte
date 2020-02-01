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

    var prevScrollpos = window.pageYOffset;
    window.onscroll = function() {
        var currentScrollPos = window.pageYOffset;
        if (prevScrollpos > currentScrollPos) {
            $("#header").css("opacity", "100");
        } else {
            $("#header").css("opacity", "0");
        }
        prevScrollpos = currentScrollPos;
    }
});
