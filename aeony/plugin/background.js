var heatmap = [];
var videoElement;
var videoId;

var didLoadPage = false;

chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
  if (msg === "new_window") {
    chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
      var url = tabs[0].url;
      if (url.startsWith("https://www.youtube.com/watch?v=")) {
        videoId = url.split('=')[1].split('&')[0];
        $.post("http://aeonplugin.tech:8000/video/" + videoId, function (result) {
          console.log(result);
        });
      }
      });
  } else if (!isNaN(msg)) {
    updateHeatmap(msg);
  }
  });

function sendMap() {
  chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
    if (tabs[0]) {
      videoId = tabs[0].url.split('=')[1];
    }
    if (heatmap.length > 1) {
    if (heatmap.includes(1)) { heatmap.unshift(0); }
      console.log(heatmap);
      var obj = {videoId: videoId, data: JSON.stringify(heatmap)};
      $.post("http://aeonplugin.tech:8000/heatmap", obj, function (result) {
          console.log(result);
      });
      heatmap = [];
    }
  });
}

function updateHeatmap(time) {
  if (time != 0) {
    heatmap.push(time); 
  }
  if (heatmap.length > 20) {
    sendMap();
  }
}

