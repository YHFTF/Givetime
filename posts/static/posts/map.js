function initMap() {
    const defaultCenter = { lat: 37.5665, lng: 126.9780 }; // Seoul
    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 12,
        center: defaultCenter,
    });

    const geocoder = new google.maps.Geocoder();
    let marker;

    function placeMarkerAndPan(latLng) {
        if (marker) marker.setMap(null);
        marker = new google.maps.Marker({
            position: latLng,
            map: map,
        });
        map.panTo(latLng);
    }

    function extractAddress(result) {
        let city = '';
        let dong = '';
        result.address_components.forEach(ac => {
            if (ac.types.includes('locality') || ac.types.includes('administrative_area_level_1')) {
                city = ac.long_name;
            }
            if (ac.types.includes('sublocality_level_2') || ac.types.includes('sublocality')) {
                dong = ac.long_name;
            }
        });
        return city && dong ? city + ' ' + dong : result.formatted_address;
    }

    map.addListener('click', function(evt) {
        placeMarkerAndPan(evt.latLng);
        geocoder.geocode({ location: evt.latLng }, function(results, status) {
            if (status === 'OK' && results[0]) {
                document.getElementById('address').value = extractAddress(results[0]);
            }
        });
    });

    const addressInput = document.getElementById('address');
    if (addressInput.value) {
        geocoder.geocode({ address: addressInput.value }, function(results, status) {
            if (status === 'OK' && results[0]) {
                placeMarkerAndPan(results[0].geometry.location);
            }
        });
    }
}

window.addEventListener('load', initMap);
