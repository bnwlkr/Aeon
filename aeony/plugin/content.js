console.log("injected"); 
var lastTime = -1;


chrome.runtime.onMessage.addListener(function(msg, sender, sendResponse) {
      var videoElement = document.querySelector('video');
      videoElement.currentTime = msg;
});

document.body.addEventListener("yt-navigate-finish", function(event) {
    chrome.runtime.sendMessage("new_window");
    var videoElement = document.querySelector('video');
    videoElement.addEventListener('timeupdate', function(event) {
      var time = parseInt(event.target.currentTime);
      if (!isAdShowing() && time != lastTime) {
        lastTime = time;
        chrome.runtime.sendMessage(time);
      }
    });
});

function isAdShowing () {
  return document.getElementsByClassName("html5-video-player")[0].attributes[0].nodeValue.includes("ad-showing");
}
