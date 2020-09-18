// 获取用户的摄像头,展示时的位置大小
var front =false;//设置一个变量来决定是否是前置摄像头 user是前置,environment是后置
//按钮变换前置后者后置摄像头
document.getElementById('change').onclick = function() { front = !front;console.log(settings) };

var settings ={
  audio:true,
  video:{
    frameRate: { ideal:10, max: 15 },
    width :1280 ,
    height:720,
    //通过三元运算符来判别前置后置摄像头
    facingMode:(front? "user" : "environment"),
  }
};
//如果旧版浏览器无mediaDevices,则先将mediaDevices设置为一个空值
if(navigator.mediaDevices === undefined){
    navigator.mediaDevices={}
}

if(navigator.mediaDevices.getUserMedia === undefined){
    navigator.mediaDevices.getUserMedia = function (settings)
    {
        //是适应旧版本浏览器
        var getUserMedia = navigator.mediaDevices.getUserMedia ||
                                        navigator.getUserMedia ||
                                        navigator.webkitGetUserMedia ||
                                        navigator.mozGetUserMedia ||
                                        navigator.msGetUserMedia;
        alert(getUserMedia);
        //如果尝试以上几种情况依旧无摄像头,则返回一个报错信息
        if (!getUserMedia){
            return Promise.reject(new Error("你的摄像头或语音权限无法获取,请使用FireFox,Chrome和尽可能高版本的浏览器"))
        }
        //否则为旧版navigator.getUserMedia方法包裹一个Promise
        return new Promise(function (resolve,reject) {
            getUserMedia.call(navigator,settings,resolve,reject)
        });
    }
}


navigator.mediaDevices.getUserMedia(settings)
    .then(function(Stream) {
    var video = document.getElementById("video")
    video.srcObject = Stream;
    video.onloadedmetadata = function (e) {
      video.play();
    };
  })
    .catch(function(err) {
    console.log(err.name + ": " + err.message);
  })
