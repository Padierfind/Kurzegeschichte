function get_story_previews_with_index(){
    var searchParams = new URLSearchParams(window.location.search)
    if(searchParams.has('index')) {
        ajax_get_story_previews(searchParams.get('index'), "");
    }else{
        ajax_get_story_previews(0, "");
    }
}

function get_selected_categories(){
    var selected_categories = [];

    var listItems = $("#category_selection li");
    listItems.each(function(idx, li) {
        var is_selected = $(li).hasClass("selected");
        if(is_selected == true){
            selected_categories.push($(li).attr('id'));
        }
    });

    return selected_categories;
}

function get_selected_lengths(){
    var selected_lengths = [];

    var listItems = $("#length_selection li");
    listItems.each(function(idx, li) {
        var is_selected = $(li).hasClass("selected");
        if(is_selected == true){
            selected_lengths.push($(li).attr('id'));
        }
    });

    return selected_lengths;
}

function get_selected_sorting(){
    var selected_sorting = "";

    var listItems = $("#sorting_selection li");
    listItems.each(function(idx, li) {
        var is_selected = $(li).hasClass("selected");
        if(is_selected == true){
            selected_sorting = $(li).attr('id');
        }
    });

    return selected_sorting;
}

function apply_filter(selected){
    $(selected).toggleClass("selected");
    get_story_previews_with_index();
}

// This function is different is different from the other filters because only one can be selected at a time.
function apply_filter_sorting(selected){
    var listItems = $("#sorting_selection li");
    listItems.each(function(idx, li) {
        $(li).removeClass("selected");
    });

    $(selected).addClass("selected");
    get_story_previews_with_index();
}

function ajax_get_story_previews(index){
    var categories = get_selected_categories();
    var lengths = get_selected_lengths();
    var sorting = get_selected_sorting();

    var db_index = index * 8;

    var url_categories = "&categories=" + categories;
    if(categories == ""){
        url_categories = "";
    }

    var url_lengths = "&lengths=" + lengths;

    if(lengths == ""){
        url_lengths = "";
    }

    var url_sorting = "&sorting=" + sorting;

    //Empty Containers
    $("#preview_container").empty();
    $("#preview_container_2").empty();


    $.ajax({
        url: "/get_story_previews/?index=" + db_index + url_categories + url_lengths + url_sorting
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

$( document ).ready(function() {
    get_story_previews_with_index();
});