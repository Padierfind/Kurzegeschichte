$( document ).ready(function() {
    var searchParams = new URLSearchParams(window.location.search)
    if(searchParams.has('index')) {
        ajax_get_story_previews(searchParams.get('index'), "");
    }else{
        ajax_get_story_previews(0, "");
    }
});

function apply_filter(index, selected_category){
    $(selected_category).toggleClass("selected");
    var selected_categories = [];

    var listItems = $("#category_selection li");
    listItems.each(function(idx, li) {
        var is_selected = $(li).hasClass("selected");
        if(is_selected == true){
            selected_categories.push($(li).attr('id'));
        }
    });

    ajax_get_story_previews(index, selected_categories)
}

function ajax_get_story_previews(index, categories){
    var db_index = index * 8;

    var url_categories = "?categories=" + categories;
    if(categories == ""){
        url_categories = "";
    }

    //Empty Containers
    $("#preview_container").empty();
    $("#preview_container_2").empty();


    $.ajax({
        url: "/get_story_previews/" + db_index + url_categories
    }).done(function (result) {
        if(result == "False"){
            display_notification("Wir haben gerade Probleme, die Geschichten aus der " +
                "Datenbank zu laden. Bitte versuche es später noch einmal.");
            return;
        }

        var total_length = result['total_length'];
        var total_length_divided = Math.ceil(total_length / 8);
        var current_page = (parseInt(index) + 1);

        if(total_length_divided == current_page){
            $("#next_page_button").attr("disabled", true);
        }
        else{
            $("#next_page_button").attr("disabled", false);
        }

        if(current_page == 1){
            $("#previous_page_button").attr("disabled", true);
        }
        else{
            $("#previous_page_button").attr("disabled", false);
        }


        $("#page_index").text(current_page +  "/" + total_length_divided);
        $("#previous_page_link").attr("href", "?index=" + (parseInt(current_page) - 2));
        $("#next_page_link").attr("href", "?index=" + (current_page));

        var previews = result['result'];

        var counter = 0;

        previews.forEach(function(element) {
            counter++;

            let title = element['title'];
            let id = element['_id'];
            let categories = element['categories'];
            let preview_text = element['preview_text'];
            let timestamp = element['timestamp'];
            let user_id = element['user_id'];
            let reading_time = element['reading_time'];

            var container = "#preview_container";

            if(counter > 4){
                container = "#preview_container_2";
            }

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