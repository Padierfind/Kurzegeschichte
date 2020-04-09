function load_story_data(){
    $.ajax({
        url: "/get_story_data_without_preview/" + story_id
    }).done(function (result) {
        if(result == "False"){
            display_notification("Wir haben gerade Probleme, die Geschichte aus der " +
                "Datenbank zu laden. Bitte versuche es später noch einmal.");
            return;
        }
        else{
            var result = result['result'];

            console.log(result)
            title = result['title'];
            content = result['content'];
            timestamp = result['timestamp'];
            user_id = result['user_id'];
            reading_time = result['reading_time'];
            console.log(content);
            length = countWords(content);
            tags = result['categories'];
    
            // Meta Tags
            $('meta[name="title"]').attr('content', title);
    
            // Page Content
            $("#story_title").text(title);
            $("#text-block-1").html(content);
            $("#reading_time").text("Lesezeit ca. " + reading_time + " Minuten")
            $("#author").html("Geschrieben von <a href=/profile?user=" + user_id.split(" ").join("%20") + ">" + user_id + ".")
            $("#timestamp").text("Veröffentlicht am " + timestamp);
            $("#length").text("Länge: " + length + " Wörter");
            
            document.title = title;
        }
        loading_flag = true;
    });
}

function change_tags(){
    var category_selection = $('#category_selection').val();
    $("#tags").text("Tags: " + category_selection);
}

function validate_form(){
    var text_field = $('#input_field_preview').val();

    if (text_field == "") {
        display_notification("Bitte gebe einen Vorschau Text ein.");
        return false;
    }

    var category_selection = $('#category_selection').val();
    var lan_conditions = ["DE", "EN"];

    var result = lan_conditions.some(el => category_selection.includes(el));

    if(result == false){
        display_notification("Bitte wähle eine Sprache in den Kategorien aus.");
        return false;    
    }

    return true;
}

function publish_story(){
    let form = $("#preview_form");

    if(validate_form() == true){
        $("#user_id").val(user_id);
        $("#title").val(title);
        $("#timestamp").val(timestamp);
        $("#story_id").val(story_id);
    
        $("#reading_time_form").val(reading_time);
        form.submit();
    }
}

$( document ).ready(function() {
    loop();
    var searchParams = new URLSearchParams(window.location.search)

    if(searchParams.has('story_id')){
        story_id = searchParams.get('story_id');

        load_story_data(story_id);
    }
    else {
        display_notification("Etwas ist schief gegangen. Diese Geschichte existiert nicht. Bitte schreibe eine Email an info@kurzegeschichte.de. Vielleicht können wir sie gemeinsam retten.");
    }

    $('#input_field_preview').bind('input propertychange', function () {

        $('#preview_text').text(this.value);

        var text_max = 250;
        var text_length = $('#input_field_preview').val().length;

        $('#text_area_feedback').html(text_length + '/' + text_max);

    });

    $(".js-select2").select2({
        placeholder: "Wähle Kategorien aus",
        theme: "material"
    });

    $('.js-select2').on('change', function() {
        var selected = "";

        $.each($(".js-select2 option:selected"), function(){
            selected += "<div class=\"tag\">" + $(this).val() + "</div>&nbsp;";
        });
        $("#categories_preview").html(selected);
    });
});