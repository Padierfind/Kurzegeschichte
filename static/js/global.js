function toggleMenu(){
    $("#menu > ul").children().not("#menu_button").toggle();
}

$( document ).ready(function() {
    $("#menu > ul").children().not("#menu_button").hide();

    var searchParams = new URLSearchParams(window.location.search)
    if(searchParams.has('notification')) {
        display_notification(searchParams.get('notification'));
    }
});

function display_notification(notification_text){
    $("#notification").text(notification_text);
    $("#notification").slideDown("slow");

    setTimeout(function() {
        $("#notification").slideUp("slow");
    }, 4500);
}