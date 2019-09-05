function toggleMenu(){
    $("#menu > ul").children().not("#menu_button").toggle();
}

$( document ).ready(function() {
    $("#menu > ul").children().not("#menu_button").hide();
});