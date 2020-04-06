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

var didScroll;
var lastScrollTop = 0;
var delta = 80;
var navbarHeight = $('header').outerHeight();

function hasScrolled() {
    var st = $(this).scrollTop();
    
    // Make sure they scroll more than delta
    if(Math.abs(lastScrollTop - st) <= delta)
        return;
    
    // If they scrolled down and are past the navbar, add class .nav-up.
    // This is necessary so you never see what is "behind" the navbar.
    if (st > lastScrollTop){
        // Scroll Down
        console.log("Scroll Down");
        $("#menu").addClass("menu_up");
        $("#logo").addClass("inv");
        $("#up_logo").removeClass("inv");
    } else {
        // Scroll Up
        if(st + $(window).height() < $(document).height()) {
            console.log("Scroll Up");
            $("#menu").removeClass("menu_up");
            $("#logo").removeClass("inv");
            $("#up_logo").addClass("inv");    
        }
    }
    
    lastScrollTop = st;
}

$( document ).ready(function() {
    $("#menu_expansion").hide();

    var searchParams = new URLSearchParams(window.location.search)
    if(searchParams.has('notification')) {
        display_notification(searchParams.get('notification'));
    }

    check_if_user_is_logged_in();
    
    $(window).scroll(function(event){
        didScroll = true;
    });
    
    setInterval(function() {
        if (didScroll) {
            hasScrolled();
            didScroll = false;
        }
    }, 250);
    
});
