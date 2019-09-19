var title, content, story_id, timestamp, user_id, reading_time;

$( document ).ready(function() {

    var searchParams = new URLSearchParams(window.location.search)
    if(searchParams.has('story_id')){
        story_id = searchParams.get('story_id');

        $.ajax({
            url: "/get_story_data/" + story_id
        }).done(function (result) {
            console.log(result);
            title = result['result']['title'];
            content = result['result']['content'];
            timestamp = result['result']['timestamp'];
            user_id = result['result']['user_id'];
            reading_time = result['result']['reading_time'];

            $("#story_title").text(title);
            $("#text-block-1").html(content);
            $("#reading_time").text("Lesezeit ca. " + reading_time + " Minuten.")
            $("#reading_time").text("Lesezeit ca. " + reading_time + " Minuten.")
            $("#author").text("Geschrieben von " + user_id + ".")

        });
    }else {
        // TODO: Throw Error
    }

});