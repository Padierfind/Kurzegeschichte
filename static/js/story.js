var title, content, story_id, timestamp, user_id, reading_time;

function disable_call_to_action(){
        $.ajax({
        url: "/get_login_status"
        }).done(function (result) {
            if(result == "False"){
                return false;
            }
        $("#call_to_action_comment").toggleClass("hidden");
        $("#write_comment").toggleClass("hidden");
    });
}

function toggleMeta(){
    $("#meta_box_hidden").toggle('fast');
}

function post_comment(){
    var searchParams = new URLSearchParams(window.location.search)

    if(searchParams.has('story_id')) {
        story_id = searchParams.get('story_id');
        let form = $("#comment_form");

        $("#story_id_form").val(story_id);
        form.submit();
    }
    else{
        display_notification("Irgendetwas stimmt hier nicht. Bitte versuche es später noch einmal.");
    }
}

function load_comments(story_id){
    $.ajax({
    url: "/get_comments/" + story_id
    }).done(function (result) {
        if(result == "False"){
            display_notification("Wir hatten Probleme damit, die Kommentare zu laden. Bitte versuche es" +
                "später erneut.");
            return false;
        }
        else{
            var previews = result['result'];
            var total_length = result['total_length'];

            var container = "#comments_box"

            if(total_length == 0){
                $(container).append(
                "<div class=\"comment\" style='text-align: center;'>" +
                    "Es wurden noch keine Kommentare zu dieser Geschichte geschrieben." +
                "</div>");
            }


            previews.forEach(function(element) {
                let timestamp = element['timestamp'];
                let user_id = element['user_id'];
                let content = element['content'];

                $(container).append(
                "<div class=\"comment\">" +
                    "<div id=\"content\" class=\"comment_content\">\n" +
                    content +
                    "</div>\n" +
                    "<div id=\"user_name\" class=\"comment_user_name\">\n" +
                    "- " + user_id + ", " + timestamp + "\n" +
                    "</div>\n" +
                "</div>");
            });
        }

    });
}

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

            load_comments(story_id);

        });
    }else {
        display_notification("Leider ist dieses Blatt noch unbeschrieben. Aber vielleicht entspringt ja " +
            "deiner Kreativität eine neue Geschichte, die diese Seite füllen könnte.");
    }

    $("#meta_box_hidden").hide();
    disable_call_to_action();
});