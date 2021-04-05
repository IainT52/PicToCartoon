
// Submits image file without a need for a submit button
var change_running = false, loadScreenVisible = false;
const loadWord = "Thinking";   

$('#img-submit').change(function() {
    if(!change_running){
        change_running = true;
        setTimeout(function(){
            showLoadScreen();
            $('#img-form').submit();
            change_running = false;
        }, 300);
    }
});

// Default image click event listener
$(".default").click(function(e) {
    showLoadScreen();
    img_id = e.target.id;
    $('#default-form').append('<input type="hidden" name="id" value="'+ img_id +'" />');
    $('#default-form').submit();
    return;
});

function showLoadScreen(){
    loadScreenVisible = true;
    $('.loader').show();
    // Load Screen thinking animation
    var colors = ["#4476ff", "#e42f2f", "#40b32a"];
    var loadInterval = window.setInterval(function(){
        if (loadScreenVisible) {
            $('.lds-ellipsis > span').each(function(){
                this.style.color = colors[Math.floor(3 * Math.random())];
            });
            // $(".lds-ellipsis").empty();
            // for (let i = 0; i < loadWord.length; i++){
            //     character = loadWord.charAt(i);
            //     var fontType = Math.ceil(3 * Math.random());
            //     $(".lds-ellipsis").append('<span class="font-' + fontType + '">' + character + "</span>");
            // }
        }
    }, 400);
}