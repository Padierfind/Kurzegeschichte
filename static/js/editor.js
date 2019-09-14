var quill;

$( document ).ready(function() {
    quill = new Quill('#editor', {
        placeholder: 'Hier fängt die Geschichte an...',
        theme: 'bubble'
    });
});

function PostContentToSaveDraft(){
    var form = $("#editor_form");
    var content = quill.root.innerHTML;
    $("#content").val(content);
    form.submit();
}