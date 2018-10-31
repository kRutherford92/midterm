var allData = [];
var stationMap;
loadData();

function loadData() {

	d3.csv("static/data/midterm.csv", function (data) {

		allData = data;
		allData.forEach(function(d){
			d.baths = +d.baths;
			d.beds = +d.beds;
			d.display_x = +d.display_x;
			d.display_y = +d.display_y;
			d.list_price = +d.list_price;
			d.mlsnum = +d.mlsnum;
			d.ppsf = +d.ppsf;
			d.predicted_price = +d.predicted_price;
			d.sqft = +d.sqft;			
		});
			createVis();
	});
}

function createVis() {
	d3.select("#station-count").text(allData.length);
	stationMap = new StationMap("station-map", allData, [0, 0]);
}