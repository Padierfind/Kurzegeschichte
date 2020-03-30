var title, content, story_id, timestamp, user_id, reading_time, length, tags;

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
        loading_flag = true;
    });
}

function countWords(txt) {
    console.log(txt);
    return txt.trim().split(/\s+/).length;
}

function load_story_data(){
    $.ajax({
        url: "/get_story_data/" + story_id
    }).done(function (result) {
        if(result == "False"){
            display_notification("Wir haben gerade Probleme, die Geschichte aus der " +
                "Datenbank zu laden. Bitte versuche es später noch einmal.");
        return;
    }

        title = result['title'];
        content = result['content'];
        timestamp = result['timestamp'];
        user_id = result['user_id'];
        reading_time = result['reading_time'];

        length = countWords(content);
        tags = result['categories'];

        // Meta Tags
        $('meta[name="title"]').attr('content', title);
        $('meta[name="keywords"]').attr('content', "Kurzgeschichte, lesen, Buch, Geschichte, " + user_id + ", " + title);
        $('meta[name="description"]').attr('content', "Jetzt " + title + " von " + user_id + " gratis auf Kurzegeschichte lesen!");
        $('meta[name="author"]').attr('content', user_id);
        $('meta[name="twitter:data1"]').attr('content', "ca. " + reading_time + " Minuten");

        $('meta[property="og:url"]').attr('content', window.location.href);
        $('meta[property="og:title"]').attr('content', title);
        $('meta[property="twitter:title"]').attr('content', title);
        $('meta[property="twitter:description"]').attr('content', 'Jetzt "' + title + '" von ' + user_id + " gratis auf Kurzegeschichte lesen!");
        $('meta[property="al:web:url"]').attr('content', window.location.href);
        $('meta[property="books:author"]').attr('content', user_id);

        // Page Content
        $("#story_title").text(title);
        $("#text-block-1").html(content);
        $("#reading_time").text("Lesezeit ca. " + reading_time + " Minuten")
        $("#author").html("Geschrieben von <a href=/profile?user=" + user_id.split(" ").join("%20") + ">" + user_id + ".")
        $("#timestamp").text("Veröffentlicht am " + timestamp);
        $("#tags").text("Tags: " + tags);
        $("#length").text("Länge: " + length + " Wörter");
        
        document.title = title;
    });
}

$( document ).ready(function() {
    loop();
    var searchParams = new URLSearchParams(window.location.search)
    if(searchParams.has('story_id')){
        story_id = searchParams.get('story_id');

        load_comments(story_id);
        load_story_data(story_id);
    }
    else {
        display_notification("Leider ist dieses Blatt noch unbeschrieben. Aber vielleicht entspringt ja " +
            "deiner Kreativität eine neue Geschichte, die diese Seite füllen könnte.");
    }

    $("#meta_box_hidden").hide();
    disable_call_to_action();
});