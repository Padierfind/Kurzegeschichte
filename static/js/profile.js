function ajax_get_user_story_previews(user_id){
    //Empty Containers
    $("#preview_container").empty();
    $("#name").text(user_id);

    $.ajax({
        url: "/get_user_story_previews/" + user_id
    }).done(function (result) {
        if(result == "False"){
            display_notification("Wir haben gerade Probleme, die Geschichten aus der " +
                "Datenbank zu laden. Bitte versuche es später noch einmal.");
            return;
        }

        var total_length = result['total_length'];

        var previews = result['result'];

        previews.forEach(function(element) {

            let title = element['title'];
            let id = element['_id'];
            let categories = element['categories'];
            let preview_text = element['preview_text'];
            let timestamp = element['timestamp'];
            let user_id = element['user_id'];
            let reading_time = element['reading_time'];

            var container = "#preview_container";


            var tags = "";

            categories.forEach(function(element){
                var url = "javascript: apply_filter('#" + element + "');"
                tags += "<div class=\"tag\"><a href='" + url + "'>#" + element + "&nbsp;</a></div>";
            });

            $(container).append(
                "<div class=\"col-sm-6 preview\">" +
                "<hr>" +
                "<div class=\"title\"><a href='/story?story_id=" + id + "'>" + title +
                "</a></div>" +
                "<div class=\"meta author\">" +
                "Geschrieben von " + user_id +
                "</div>    " +
                "<p>" +
                    preview_text +
                "</p>" +
                "" +
                "<div class=\"col-sm-8 meta\">" +
                tags +
                "    <div>" +
                "        Lesezeit ca. " + reading_time + " Minuten" +
                "    </div>" +
                "</div>" +
                "<div class='col-sm-4 readmore'><a href='/story?story_id=" + id + "'>Lesen</a></div>" +
                "</div>" );
        });
    });
}

$( document ).ready(function() {
    var searchParams = new URLSearchParams(window.location.search);

    if(searchParams.has('user')) {
        ajax_get_user_story_previews(searchParams.get('user'));
    }else{
        display_notification('Es wurde kein Nutzer angegeben.');
    }
});