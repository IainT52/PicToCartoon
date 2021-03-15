const sentence = "What happens when a Neural Network # tries to draw your photo?"
const credits = "A fun project made by Iain Tierney."

var intervalId = window.setInterval(function(){
    $(".hand").empty();
    for (let i = 0; i < sentence.length; i++){
        character = sentence.charAt(i);
        var fontType = Math.ceil(3 * Math.random());

        if (character === '#'){
            $(".hand").append('<br>');
        }
        else{
            $(".hand").append('<span class="font-' + fontType + '">' + character + "</span>");
        }

    }
  }, 1500);

// Used to create a doodle from a given sentence
function createDoodleFromSentence(sentence) {
    for (let i = 0; i < sentence.length; i++){
        character = sentence.charAt(i);
        var fontType = Math.ceil(3 * Math.random());
    
        if (character === '#'){
            $(".credits").append('<br>');
        }
        else{
            $(".credits").append('<span class="font-' + fontType + '">' + character + "</span>");
        }
    }
}
