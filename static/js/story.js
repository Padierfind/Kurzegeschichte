$( document ).ready(function() {

    var searchParams = new URLSearchParams(window.location.search)

    if(searchParams.has('story_id')){
        var story_id = searchParams.get('story_id');

        $.ajax({
            url: "/get_story_data/" + story_id
        }).done(function (result) {
            var title = result['result']['title'];
            var content = result['result']['content'];

            $("#story_title").text(title);
            $("#text-block-1").html(content);
        });
    }else {
        // TODO: Throw Error
    }
});