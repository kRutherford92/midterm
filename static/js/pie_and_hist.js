// data, xScale, yScale, rad variables
// load data with d3.json("/load_data", function (data)

d3.json("/load_data", function(data){

// define variable scatter_data

data = data['condos'];

// group data using d3.nest()
var bedrooms_data = d3.nest()
.key(function(d){
  return d.beds;
})
.rollup(function(v){
  return v.length;
})
.entries(data);

// define svg, margin, width, height, and g elements
var svg = d3.select("#donutChart").attr('class', 'pie')
  margin = {top: 0, right: 30, bottom: 30, left: 30},
  width = +svg.attr("width") - margin.left - margin.right,
  height = +svg.attr("height") - margin.top - margin.bottom,
  g = svg.append("g")
    .attr("transform", "translate(" + (width/1.6) + "," + (height/1.73) + ")");

  var text = "";

  var width = svg.attr("width");
  var height = svg.attr("height");
  var thickness = 50;
  var duration = 500;


  // define radius and color
  var radius = Math.min(width, height) / 2;
  var color = d3.scaleOrdinal()
  .domain(bedrooms_data.keys())
  .range([
    
'#6e3535',
'#d94801',
'#f16913',
'#fd8d3c',
'#fdae6b',
'#fdd0a2'

  ]);



// create arc
var arc = d3.arc()
.innerRadius(radius-thickness)
.outerRadius(radius);

// create pie
var pie = d3.pie()
.value(function(d){
  return d.value;
})
.sort(null);

// create path, append g element, add mouseover, mouseout and click functionality 
var path = g.selectAll('path')
.data(pie(bedrooms_data))
.enter()
.append("g")
.on("mouseover", function(d){
  let g = d3.select(this)
  .style("cursor", "pointer")
  .style("fill", "black")
  .append("g")
  .attr("class", "text-group");

  g.append("text")
  .attr("class", "name-text")
  .text(`${d.data.key}`+"-bedroom")
  .attr('text-anchor', 'middle')
  .attr('dy', '-1.2em');

  g.append("text")
  .attr("class", "value-text")
  .text("total condos: "+`${d.data.value}`)
  .attr('text-anchor', 'middle')
  .attr('dy', '.6em');
})
.on("mouseout", function(d){
  d3.select(this)
  .style("cursor", "none")
  .style("fill", color(this._current))
  .select(".text-group").remove();
})
.on("click", function(d){
  var scatterData = new Array();
  var i = 0;
  for(c=0;c<data.length;c++){
    if(data[c].beds==d.data.key){
      scatterData[i++]=data[c];
    }
  }
  //updateScatter(scatterData, data);
  updateScatter(d.data.key);
})
.append('path')
.attr('d', arc)
.attr('fill', (d,i) => color(i))
.on("mouseover", function(d){
  d3.select(this)
  .transition()
  .duration(400)
  .style("d", arc)
  .style("cursor", "pointer")
  .style("fill", "#324352");
})
.on("mouseout", function(d){
  d3.select(this)
  .transition()
  .duration(750)
  .attr("d", arc)
  .style("cursor", "none")
  .style("fill", color(this._current));
})
.each(function(d,i){
  this._current = i;
});
});

//////////////////////////////////// SCATTER-PLOT CODE START HERE ///////////////////////////////////
  // load condo database into javascript
  d3.json("/load_data", function(data){
    data = data['condos'];

    // convert from strings to numerical values
    data.forEach(function(d){
      d.predicted_price = +d.predicted_price;
      d.list_price = +d.list_price;
      d.baths = +d.baths;
    });
  //create svg, margin, width, height, g
  var svg = d3.select("#scatterChart");
    margin = {top: 20, right: 10, bottom: 50, left: 60},
    width = +svg.attr("width")-margin.left-margin.right,
    height = +svg.attr("height")-margin.top-margin.bottom,
    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // call xScale
  var xScale = d3.scaleLinear()
  .domain(d3.extent(data, function(d){
    return d.predicted_price;
  }))
  .range([0, width]);
  // call yScale
  var yScale = d3.scaleLinear()
  .domain(d3.extent(data, function(d){
    return d.list_price;
  }))
  .range([height, 0]);
  // call rad (stands for radius)
  var radius = d3.scaleSqrt()
  .range([2,5])
  .domain(d3.extent(data, function(d){
    return d.baths/8;
  })).nice();
  // create xAxis
  var xAxis = d3.axisBottom()
  .scale(xScale)
  .ticks(3);

  // create yAxis
  var yAxis = d3.axisLeft()
  .scale(yScale)
  .ticks(5);

  // append xAxis in g
  g.append("g")
  .attr("transform", "translate(0,"+height+")")
  .call(xAxis);
  // append yAxis in g
  g.append("g")
  .call(yAxis);
  // create bubble variable, append circle, define attributes
  var bubble = g.selectAll("circle")
  .data(data)
  .enter()
  .append("circle")
  .attr("class", "bubble")
  .attr("cx", function(d){
    return xScale(d.predicted_price);
  })
  .attr("cy", function(d){
    return yScale(d.list_price);
  })
  .attr("r", function(d){
    return radius(d.baths);
  })
  .style("fill", "#0973C8")
  .style("fill-opacity", 0.5)
  // append both axis labes into g
  bubble.attr("transform", "translate(30,15)scale(0.85)");

  g.append("text")
  .attr("transform", "rotate(-90)")
  .attr('x', -90)
  .attr('y', 15)
  .attr('class', 'label')
  .text('Listed Price');

  g.append("text")
  .attr('x', (width/2)+60)
  .attr('y', height+35)
  .attr('text-anchor', 'end')
  .attr('class', 'label')
  .text('Predicted Price')

  });

// update scatterplot with only data for condos with a specific number of bedrooms
function updateScatter(scatter_data){
    // select scatterPlot to update data
    var svg = d3.select("#scatterChart");

    // select all of the circles in scatterChart
    var circle = svg.selectAll("circle")
    // specify data to be the new scatter_data
    .style("fill-opacity", function(d){
      if(d.beds==scatter_data){
        return 0.5;
      } else {
        return 0;
      }
    })
}