$( document ).ready(function() {
    var searchParams = new URLSearchParams(window.location.search)
    if(searchParams.has('index')) {

    }else{
        ajax_get_story_previews(0);
    }
});

function ajax_get_story_previews(index){
    $.ajax({
        url: "/get_story_previews/" + index
    }).done(function (result) {
        if(result == "False"){
            display_notification("Wir haben gerade Probleme, die Geschichten aus der " +
                "Datenbank zu laden. Bitte versuche es später noch einmal.");
            return;
        }

        var previews = result['result'];

        previews.forEach(function(element) {

            let title = element['title'];
            let id = element['_id'];
            let categories = element['categories'];
            let preview_text = element['preview_text'];
            let timestamp = element['timestamp'];
            let user_id = element['user_id'];
            let reading_time = element['reading_time'];

            $( "#preview_container" ).append(
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
                "    <div class=\"tag\">" +
                "        #Romantik" +
                "    </div>" +
                "    <div class=\"tag\">" +
                "        #Krimi" +
                "    </div>" +
                "    <div>" +
                "        Lesezeit ca. " + reading_time + " Minuten" +
                "    </div>" +
                "</div>" +
                "<div class='col-sm-4 readmore'><a href='/story?story_id=" + id + "'>Lesen</a></div>" +
                "</div>" );
        });
    });
}