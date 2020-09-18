//匿名函数
(function (){
var width =320;
var height =0;

var streaming =false;

var video =null;
var canvas = null;
var photos =null;
var startbutton = null;

function startup() {
    video =document.getElementById("video");
    canvas =document.getElementById("canvas");
    photos =document.getElementById("photo");
    startbutton =document.getElementById("startbutton")
    navigator.mediaDevices.getUserMedia({video:{facingMode:"environment"},audio:true})
        .then(function (stream) {
            video.srcObject =stream;
            video.play()
        })
        .catch(function (err) {
            console.log("发生错误"+err)
        });
    video.addEventListener("canplay",function (event) {
        if(!streaming){
            height =video.videoHeight/(video.videoWidth/width)
            if (isNaN(height)) {
            height = width / (4/3);
            }
            video.setAttribute("width",width);
            video.setAttribute("height",height);
            canvas.setAttribute("width",width);
            canvas.setAttribute("height",height);
            streaming= true;
        }
    },false);
    startbutton.addEventListener("click",function (event) {
        takepicture();
        event.preventDefault();
    },false);
    clearphotos();
}
function clearphotos() {
    var context =canvas.getContext("2d");
    if (width && height){
        canvas.width =width;
        canvas.height =height;
        context.drawImage(video,0,0,width,height);
        var data =canvas.toDataURL("image/png");
        photos.setAttribute("src",data);
    }else {clearphotos();}
};
function takepicture() {
    var context = canvas.getContext('2d');
    if (width && height) {
        canvas.width = width;
        canvas.height = height;
        context.drawImage(video, 0, 0, width, height);

        var data = canvas.toDataURL('image/png');
        photo.setAttribute('src', data);
    } else {
        clearphoto();
    }
};
window.addEventListener("load",startup,false);
})();
