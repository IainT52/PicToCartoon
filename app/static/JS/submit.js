
// Submits image file without a need for a submit button
var change_running = false;    

$('#img-submit').change(function() {
    if(!change_running){
        change_running = true;
        setTimeout(function(){
            console.log("double_test");
            $('#img-form').submit();
            change_running = false;
        }, 300);
    }
});

// Default image click event listener
$(".default").click(function(e) {
    img_id = e.target.id;
    $('#default-form').append('<input type="hidden" name="id" value="'+ img_id +'" />');
    $('#default-form').submit();
    return;
});