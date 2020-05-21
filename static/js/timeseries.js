
// todo: checkboxes for each state (or select all)
// todo: 7day moving average
// todo: N-day moving average
// todo: N-day rate of change
// todo: state sum
// todo: deaths per capita

var dat;

$(document).ready(function() {
    // bind to the submit button
    $('input').click(function () {
        var selected = $('#states-select').val();
        window.location = '/?states=' + selected.join();
    })
});


function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

// read the selected states via url parameter
var states = getParameterByName('states');
if (states == null) {
    states = [];
} else { states = states.split(",");}

var margin = {top: 20, right: 80, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var parseDate = d3.time.format("%Y%m%d").parse;

var x = d3.time.scale()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var color = d3.scale.category10();

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var svg = d3.select("#plot")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var lineFunction = d3.svg.line()
    .x(function(d) { 
        return x(d.date); 
    })
    .y(function(d) {
        return y(d.num);
    })
    .interpolate("linear");

function filter_selected(data) {

    // filter to the states defined in the select box
    var selected = $('#states-select').val();
    var cities = data.filter(function(x) {
        return states.includes(x.name);
    })
    return cities;

}

d3.tsv("/static/dat/covid-deaths.tsv", function(error, data) {
  color.domain(d3.keys(data[0]).filter(function(key) { return key !== "date"; }));

  data.forEach(function(d) {
    d.date = parseDate(d.date);
  });

  var cities = color.domain().map(function(name) {
      var lname = name.toLowerCase().replace(' ', '_');
        return {
          name: lname,
          values: data.map(function(d) {
            return {date: d.date, num: +d[name]};
          })
        };
  });



    // populate states select-box
    var sel = document.getElementById('states-select');
    for (var i=0; i < cities.length; i++) {
        // create new option element
        var state = cities[i].name;
        var opt = document.createElement('option');
        opt.appendChild( document.createTextNode(state) );
        opt.value = state; 
        sel.appendChild(opt);
    }

    var filtered = filter_selected(cities);
    // filter to the states defined in the url
    var cities = cities.filter(function(x) {
        return states.includes(x.name);
    })

  x.domain(d3.extent(data, function(d) {
      return d.date; 
  }));

  y.domain([
    d3.min(cities, function(c) {
        return d3.min(c.values, function(v) {
            return v.num;
        });
    }),
    d3.max(cities, function(c) { 
        return d3.max(c.values, function(v) {
            return v.num; 
        }); 
    })
  ]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("COVID-19 Deaths");

  var city = svg.selectAll(".city")
      .data(cities)
    .enter().append("g")
      .attr("class", "city");

  var graph = city.append("path")
      .attr("class", "line")
      .attr("d", function(d) { 
          var lf = lineFunction(d.values);
          return lf;
      })
//    .attr("stroke", "blue")
//    .attr("stroke-width", 2)
//    .attr("fill", "none");
      .attr("data-legend",function(d) {
          return d.name
      })
      .style("stroke", function(d) {
          return color(d.name); 
      });

  city.append("text")
      .datum(function(d) { 
          return {
              name: d.name, value: d.values[d.values.length - 1]
          }; 
      })
      .attr("transform", function(d) { 
          return "translate(" + x(d.value.date) + "," + y(d.value.num) + ")"; 
      })
      .attr("x", 3)
      .attr("dy", ".35em")
      .text(function(d) { 
          return d.name;
      });


  legend = svg.append("g")
    .attr("class","legend")
    .attr("transform","translate(50,30)")
    .style("font-size","12px")
    .call(d3.legend)

  setTimeout(function() { 
    legend
      .style("font-size","20px")
      .attr("data-style-padding",10)
      .call(d3.legend)
  },1000)

});

