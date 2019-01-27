var loadingSize = 40;
var canvasWidth = 500;
var canvasHeight = 200;

var container = document.getElementById("container");
var loadingImg = document.createElement("img");
loadingImg.src = "rolling.gif"; 
loadingImg.style.width = loadingSize + "px";
loadingImg.style.marginLeft = (canvasWidth/2 - loadingSize/2) + "px"; 
loadingImg.style.marginTop = (canvasHeight/2 - loadingSize/2) + "px";    
container.appendChild(loadingImg);


chrome.runtime.onMessage.addListener(function(msg, sender, sendResponse) {
  if (msg == "new_window") {
    everything();
  }
  });

everything();

function everything () {
  /*  WHEN PLUGIN IS OPENED, check for current video  */

  chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
      var url = tabs[0].url;
      var videoIdF = url.split('=')[1];
      if (!videoIdF) { notOnYoutube(); return; }
      var videoId = videoIdF.split('&')[0];
      if (url.startsWith("https://www.youtube.com/watch?v=")) {
        console.log("sending message");
        $.post("http://aeonplugin.tech:8000/video/" + videoId, function (result) {
          console.log(result);
          if (result === "nope") {firstTime();} else {addChart(result);}
        });
      } else {
        notOnYoutube();
      }
  });


  /* FUNCTIONS */
  function notOnYoutube () {
    var h = document.createElement("H2")                // Create a <h1> element
    var t = document.createTextNode("You're not on YouTube!");     // Create a text node
    h.style.width = 500 + "px";
    h.style.marginLeft = (canvasWidth/2 - 105) + "px"; 
    h.style.marginTop = "150px";
    h.appendChild(t);
    container.appendChild(h);
    container.removeChild(loadingImg);
  }

  function firstTime () {
    var h = document.createElement("H2")                // Create a <h1> element
    var t = document.createTextNode("First one here!");     // Create a text node
    h.style.width = 500 + "px";
    h.style.marginLeft = (canvasWidth/2 - 75) + "px"; 
    h.style.marginTop = "150px";
    h.appendChild(t);
    container.appendChild(h);
    container.removeChild(loadingImg);
  }

  function addChart(data) {
    heatmapData = [];
    var i;
    var max = 1;
    var dict = {};
    for (i = 0; i < data.heatmap.length; i++) { 
      var y = data.heatmap[i]
      heatmapData[i] = [i * 1000, y];
      if (max < y) {
        max = y;
      }
    }
    data.comments.forEach(function (c) {
      var x = parseInt(Object.keys(c)[0]);
      if (typeof dict[x] !== "undefined") {
        dict[x] += 1;
      } else {
        dict[x] = 1;
      }
    });
    console.log(dict)
    console.log(Object.keys(dict))
    var vmax = 1;
    for (i = 0; i < Object.keys(dict).length; i++) {
      var k = Object.keys(dict)[i];
      if (dict[k] > vmax) {
        argmax = k;
        vmax = dict[k];
      }
    }
    console.log(vmax)
    console.log(max)
    hist = []
    var tn = [{
      point: {
        x: parseInt(data.thumbnail) * 1000, 
        y: heatmapData[parseInt(data.thumbnail)][1],
        xAxis: 0,
        yAxis: 0,
        allowDragY: false,
        allowDragX: false,
        anchorX: "center",
        anchorY: "center"
        }, 
        text: "Thumbnail"}];
    data.comments.forEach(function (c) {
      var x = parseInt(Object.keys(c)[0]);
      hist.push([x * 1000, max / vmax]);
    });
    function sort(a, b) {
      return a[0] - b[0];
    }
    hist.sort(sort);
    console.log(hist);
    console.log(tn);

    Highcharts.stockChart('container', {
      credits: {enabled: false},
      plotOptions: {
          series: {
              cursor: 'pointer',
              events: {
                  click: function (e) {
                      chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
                        chrome.tabs.sendMessage(tabs[0].id, e.point.x / 1000);
                      });
                  }
              },
              pointWidth: 4
          }
      },
      annotations: [{
          labels: tn,
          labelOptions: {
            backgroundColor: 'rgba(207, 55, 33, 1.0)',
            borderWidth: 0
          }
      }],
      tooltip: { enabled: false },
      title: {
        text: data.title
      },
      scrollbar: {
              enabled: false
      },
      navigator: {
              enabled: false
      },
      xAxis: {
        dateTimeLabelFormats: { 
            second: '%M:%S',
            minute: '%M:%S',
            hour: '%M:%S',
            day: '%M:%S',
            week: '%M:%S',
            month: '%M:%S',
            year: '%M:%S'
          },
        visible: true
      },
      yAxis : {
        visible: false
      },
      rangeSelector: {
        enabled: false
      },
      exporting: {
          enabled: false
      },
      series: [{
        name: 'Viewers',
        type: 'area',
        data: heatmapData,
        gapSize: 1,
        tooltip: {
          valueDecimals: 1
        },
        fillColor: {
          linearGradient: {
            x1: 0,
            y1: 0,
            x2: 0,
            y2: 1
          },
          
          stops: [
            [0, Highcharts.getOptions().colors[0]],
            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
          ]
        },
        threshold: null
      },
      {
      type: "column",
      name: "Comments",
      data: hist,
      color: 'rgba(244, 193, 73,1.0)'
      }
      ],
      legend: {
          align: 'right',
          verticalAlign: 'top',
          layout: 'vertical',
      }
    });
  }
  }

