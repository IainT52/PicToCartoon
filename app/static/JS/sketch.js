// Init Variables 
var strokeIndex = 0, index = 0, i= 0, strokeObjectData, objectData, strokesForEachObject, prevx, prevy, img_width, img_height, img_scale_x, img_scale_y, x_norm, y_norm;
// Init constants
const canvasWidth = 1200, canvasHeight = 700;


function getStrokeData(data){
    strokeObjectData = $.parseJSON(data);
    objectData = strokeObjectData[0];
    img_width = objectData[i]["img_width"];
    img_height = objectData[i]["img_height"];
    img_scale_x = objectData[i]["scale"][0];
    img_scale_y = objectData[i]["scale"][1];
    x_norm = objectData[i]["normalized"][0];
    y_norm = objectData[i]["normalized"][1];
    strokesForEachObject = strokeObjectData[1][i];
    return;
}

// Setup the canvas
function setup() {
    createCanvas(canvasWidth, canvasHeight);
    background(51);
}

/* 
 * Equations to normalize scale the x and y points of each stroke coordinate.
 * x point scaled and normalized = ((cartoon_point_x / cartoon_img_width) * img_scale_x * img_width) + (x_norm*canvas_width) -> ((100/255)*.30*1200) + (.5*1200)
 * y point scaled and normalized = ((cartoon_point_y / cartoon_img_height) * img_scale_y * img_height) + (y_norm*canvas_height) -> ((100/255)*0.98*700) + (.015*700) 
 */
function draw() {
    if (strokesForEachObject) {
        console.log("draw");
        let x = strokesForEachObject[strokeIndex][index][0];
        let y = strokesForEachObject[strokeIndex][index][1];
        x = ((x / canvasWidth) * img_scale_x * img_width) + (x_norm * canvasWidth);
        y = ((y / canvasHeight) * img_scale_y * img_height) + (y_norm * canvasHeight);
        stroke(0);
        strokeWeight(3);
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
                    console.log(i);
                    img_width = objectData[i]["img_width"];
                    img_height = objectData[i]["img_height"];
                    img_scale_x = objectData[i]["scale"][0];
                    img_scale_y = objectData[i]["scale"][1];
                    x_norm = objectData[i]["normalized"][0];
                    y_norm = objectData[i]["normalized"][1];
                    console.log(img_width, img_scale_x, img_scale_y, x_norm, y_norm);
                    strokesForEachObject = strokeObjectData[1][i];
                }
            }
        } else {
            prevx = x;
            prevy = y;
        }
    }
}