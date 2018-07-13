let portfolio_chart = null;
btc_pct = parseFloat(btc_pct);
bch_pct = parseFloat(bch_pct);
eth_pct = parseFloat(eth_pct);
ltc_pct = parseFloat(ltc_pct);
cash_pct = parseFloat(cash_pct);
$(function () {
    console.log(btc_pct);
    portfolio_chart = Highcharts.chart('portfolio-chart', {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
          },
          title: {
            text: ''
          },
          tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
          },
          plotOptions: {
            pie: {
              cursor: 'pointer',
              dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                style: {
                    color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                }
              }
            }
          },
          series: [{
            name: 'Portfolio',
            colorByPoint: true,
            data: [{
              name: 'BTC',
              y: btc_pct
            }, {
              name: 'ETH',
              y: eth_pct
            }, {
              name: 'BCH',
              y: bch_pct
            }, {
              name: 'LTC',
              y: ltc_pct
            }, {
              name: 'USD',
              y: cash_pct
            }]
        }]
    });
});

$(window).resize(function() {
  portfolio_chart.redraw();
});