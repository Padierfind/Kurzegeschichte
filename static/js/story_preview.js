$( document ).ready(function() {

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