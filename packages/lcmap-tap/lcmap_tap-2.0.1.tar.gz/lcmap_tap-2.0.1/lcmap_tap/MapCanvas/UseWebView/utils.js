window.onload = function(){
    var mapDiv = 'mapL';

    var map = L.map(mapDiv, {
        center: [39.8333, -98.5833],
        zoom: 4,
        dragging: true,
        scrollWheelZoom: true,
        proxyHost: 'http://srtm.webglearth.com/cgi-bin/corsproxy.fcgi?url='
    });

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            maxZoom: 18,
            id: 'mapbox.satellite',
            accessToken: 'pk.eyJ1IjoiZHplbGVuYWsiLCJhIjoiY2pqa2VpeWd3MTB0azNxbnowdmNyeG9qMiJ9.9S-ZHbulHg6aB9R5vM4cCg'
        }).addTo(map);

    var tileOptions = {
        "color": "#0066ff",
        "weight": 1.5,
        "opacity": 1,
        "fillOpacity": 0
    };

    var markerOptions = {
        radius: 4,
        fillColor: "#00ff33",
        color: "#336600",
        weight: 1,
        opacity: 0.8,
        fillOpacity: 0.5
    }

    // Enable interactions with python using the
    function onEachFeatureHandler(feature, layer){
        layer.on('click', function(e){
            MapCanvas.onPointChanged(e.latlng.lat, e.latlng.lng);
            new L.CircleMarker(e.latlng, markerOptions).addTo(map);
        });
    }

    // hv_tiles var provided by external javascript file loaded by index.html
    overlay = L.geoJson(hv_tiles, {
        onEachFeature: onEachFeatureHandler,
        style: tileOptions
    }).addTo(map);

}