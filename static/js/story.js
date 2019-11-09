var title, content, story_id, timestamp, user_id, reading_time;

$( document ).ready(function() {
    var searchParams = new URLSearchParams(window.location.search)
    if(searchParams.has('story_id')){
        story_id = searchParams.get('story_id');

        $.ajax({
            url: "/get_story_data/" + story_id
        }).done(function (result) {
            if(result == "False"){
                display_notification("Wir haben gerade Probleme, die Geschichte aus der " +
                    "Datenbank zu laden. Bitte versuche es später noch einmal.");
            return;
        }

            title = result['result']['title'];
            content = result['result']['content'];
            timestamp = result['result']['timestamp'];
            user_id = result['result']['user_id'];
            reading_time = result['result']['reading_time'];

            $("#story_title").text(title);
            $("#text-block-1").html(content);
            $("#reading_time").text("Lesezeit ca. " + reading_time + " Minuten.")
            $("#author").html("Geschrieben von <a href=/profile?user=" + user_id + ">" + user_id + ".")
            //TODO: Meta Informationen darstellen.
        });
    }else {
        display_notification("Leider ist dieses Blatt noch unbeschrieben. Aber vielleicht entspringt ja " +
            "deiner Kreativität eine neue Geschichte, die diese Seite füllen könnte.");
    }


    $("#meta_box_hidden").hide();
});

function toggleMeta(){
    $("#meta_box_hidden").toggle('fast');
}