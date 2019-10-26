function toggleMenu(){
    $("#menu_expansion").toggle('slow');
}

$( document ).ready(function() {
    $("#menu_expansion").hide();

    var searchParams = new URLSearchParams(window.location.search)
    if(searchParams.has('notification')) {
        display_notification(searchParams.get('notification'));
    }
});

function display_notification(notification_text){
    $("#notification").text(notification_text);
    $("#notification").slideDown("fast");

    setTimeout(function() {
        $("#notification").slideUp("fast");
    }, 4500);
}