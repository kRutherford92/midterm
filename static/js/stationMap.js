
StationMap = function(_parentElement, _data, _mapPosition) {
	this.parentElement = _parentElement;
  	this.data = _data;
  	this.mapPosition = _mapPosition;

  	this.initVis();
};

StationMap.prototype.initVis = function() {

	var vis = this;
	vis.map = L.map(vis.parentElement).setView(vis.mapPosition, 8);
	L.Icon.Default.imagePath = 'static/img';

	L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}.{ext}', {
		attribution: 'Map tiles by <a href="https://stamen.com">Stamen Design</a>, <a href="https://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
		subdomains: 'abcd',
		ext: 'png'
	}).addTo(vis.map);

	vis.allMarker = L.layerGroup().addTo(vis.map);

	var LeafIcon = L.Icon.extend({
    options: {
        shadowUrl: 'static/img/marker-shadow.png',
        iconSize: [25, 41], 
    		iconAnchor: [12, 41], 
    		popupAnchor: [0, -28] 
    }
	});

	vis.redMarker = new LeafIcon({iconUrl:  'static/img/marker-red.png'});
	vis.blueMarker = new LeafIcon({iconUrl:  'static/img/marker-blue.png'});
	vis.wrangleData();
};

StationMap.prototype.wrangleData = function() {
	var vis = this;

	vis.displayData = vis.data;

    vis.updateVis();
};

StationMap.prototype.updateVis = function() {
	var vis = this;

	vis.allMarker.clearLayers();

	vis.displayData.forEach(function(d){

		var popupContent = 	'<strong>' + d.mlsnum + '</strong><br/>';
				popupContent +=	'Bath: ' + d.baths;
				popupContent +=	' Bed: ' + d.beds + '<br/>';
				popupContent +=	'<a style="color:darkred; font-weight:bold" href="/info/' + d.mlsnum + '">' + 'More Details' + '</a>';

		var markerColor = vis.blueMarker;

		var marker = L.marker([d.display_y, d.display_x], { icon: markerColor })
				.addTo(vis.map)
				.bindPopup(popupContent)
				.openPopup();

		vis.allMarker.addLayer(marker);
		
	});
};