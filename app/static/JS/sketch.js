// Init Variables 
var strokeIndex = 0, index = 0, i= 0, canvasWidth = $(window).width() * .85, canvasHeight = $(window).height() * .85, curStrokeData,
objectData, strokesForEachObject, prevx, prevy, img_width, img_height, img_scale_x, img_scale_y, x_norm, y_norm, strokeScaleForDrawTime,
detectedImg, imgOnPage = false;
// Init constants
const cartoon_img_height = 255, cartoon_img_width = 255, minFrameRate = 20, maxFrameRate = 60;

// Update canvas on window resize
$(window).resize(function() {
    canvasWidth = $(window).width() * .85;
    canvasHeight = $(window).height() * .85;
    setup();
});


function getStrokeData(data){
    curStrokeData = data;
    objectData = $.parseJSON(data)[0];
    detectedImg = new Image();
    detectedImg.src = "data:image/jpeg;base64," + $.parseJSON(data)[1];
    if (objectData.length === 0){
        displayObjectNames("No Objects Detected");
    }
    else {
        getNewObject();
    }
}


// Event listener for Redraw function
$( ".redraw" ).click(function() {
    $('p').remove('.object-names');
    object_list = new Set();
    setup();
    i=0, strokeIndex = 0, index = 0, prevx = undefined, prevy = undefined;
    getStrokeData(curStrokeData);
});


// Event listener for the view image button
$( "#view-img" ).click(function() {
    if (imgOnPage){
        $( ".detected-img" ).remove();
        imgOnPage = false;
        $("#view-img").empty();
        $("#view-img").append('<span class="font-1">Vi</span><span class="font-2">ew </span><span class="font-3">Im</span><span class="font-1">ag</span><span class="font-1">e</span>');
    }
    else{
        let width = detectedImg.naturalWidth;
        let height = detectedImg.naturalHeight;
        let minScreenDimension = Math.min($(window).height(), $(window).width());
        if (height > width){
            let widthScale = width/height;
            let heightScale = (1 * minScreenDimension)/minScreenDimension;
            let new_height = ($(window).height() * .5)*(heightScale);
            detectedImg.height = new_height;
            detectedImg.width = new_height*widthScale;
        }
        else{
            let heightScale = height/width;
            let widthScale = 1;
            let new_width = ($(window).height() * .5)*(widthScale);
            detectedImg.height = new_width*heightScale;
            detectedImg.width = new_width;
        }
        // jQuery mobile and tablet browser detection
        (function(a){(jQuery.browser=jQuery.browser||{}).mobile=/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od|ad)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))})(navigator.userAgent||navigator.vendor||window.opera);
        if (jQuery.browser.mobile){
            detectedImg.style.bottom = 0;
            detectedImg.style.left = 0;
            detectedImg.style.top = "auto";
            detectedImg.style.right = "auto";
        }
        else{
            detectedImg.style.top = 0;
            detectedImg.style.left = 0;
            detectedImg.style.right = "auto";
            detectedImg.style.bottom = "auto";
        }
        detectedImg.className = "detected-img";
        $("body").append(detectedImg);
        dragElement(detectedImg);
        $("#view-img").empty();
        $("#view-img").append('<span class="font-1">Hi</span><span class="font-2">de </span><span class="font-3">Im</span><span class="font-1">ag</span><span class="font-1">e</span>');
        imgOnPage = true;
    }
});


function displayObjectNames(name){
    $('#object-container').append('<p class="object-names '+ name +'">'+ name.replace(/_/g, ' ') +'</p>');
    $('.'+ name).fadeOut(3000);
}


function getNewObject(){
    let name =  objectData[i]["name"].replace(/ /g,"_");
    displayObjectNames(name);
    img_width = objectData[i]["img_width"];
    img_height = objectData[i]["img_height"];
    img_scale_x = objectData[i]["scale"][0];
    img_scale_y = objectData[i]["scale"][1];
    x_norm = objectData[i]["normalized"][0];
    y_norm = objectData[i]["normalized"][1];
    strokesForEachObject = objectData[i]["strokes"];
}


// Setup the canvas
function setup() {
    let renderer = createCanvas(canvasWidth, canvasHeight);
    renderer.parent("canvas-container");
    background(51);
    frameRate(60);
}

/* 
 * Equations to normalize scale the x and y points of each stroke coordinate.
 * x point scaled and normalized = ((cartoon_point_x / cartoon_img_width) * (img_scale_x * img_width)) + (x_norm*canvas_width)
 * y point scaled and normalized = ((cartoon_point_y / cartoon_img_height) * (img_scale_y * img_height)) + (y_norm*canvas_height)
 */
function draw() {
    if (strokesForEachObject) {
        let x = strokesForEachObject[strokeIndex][index][0];
        let y = strokesForEachObject[strokeIndex][index][1];
        x = ((x / cartoon_img_height) * (img_scale_x * canvasWidth)) + (x_norm * canvasWidth);
        y = ((y / cartoon_img_width) * (img_scale_y * canvasHeight)) + (y_norm * canvasHeight);
        stroke(255);
        strokeWeight(max(.8,5*((img_scale_x + img_scale_y)/1.3)));
        if (prevx !== undefined) {
            line(prevx, prevy, x, y);
        }
        index++;
        if (index === strokesForEachObject[strokeIndex].length) {
            strokeIndex++;
            prevx = undefined;
            prevy = undefined;
            index = 0;
            if (strokeIndex === strokesForEachObject.length) {
                strokesForEachObject = undefined;
                strokeIndex = 0;
                i++;
                if (i < objectData.length){
                    getNewObject();
                }
                else{
                    i=0, strokeIndex = 0, index = 0, prevx = undefined, prevy = undefined;
                }
            }
        } else {
            prevx = x;
            prevy = y;
        }
    }
}