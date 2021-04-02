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
            console.log($(window).height(), new_width);
            detectedImg.height = new_width*heightScale;
            detectedImg.width = new_width;
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