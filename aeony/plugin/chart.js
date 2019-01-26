$.getJSON('https://cdn.rawgit.com/highcharts/highcharts/057b672172ccc6c08fe7dbb27fc17ebca3f5b770/samples/data/new-intraday.json', function (data) {
  console.log(data);
  // create the chart
  Highcharts.stockChart('container', {

    credits: {enabled: false},
    plotOptions: {
        series: {
            cursor: 'pointer',
            events: {
                click: function (e) {
                    console.log(e["point"]["x"]);
                }
            }
        }
    },
    title: {
      text: 'Video Title'
    },
    scrollbar: {
            enabled: false
    },
    navigator: {
            enabled: false
    },

    xAxis: {
      gapGridLineWidth: 0
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
      data: data,
      gapSize: 5,
      tooltip: {
        valueDecimals: 3
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
    }]
  });
});

