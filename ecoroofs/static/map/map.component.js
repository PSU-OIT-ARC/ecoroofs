const MapComponent = {
    controller: function (map) {
        const target = document.querySelector('ecoroofs-map');
        map.setTarget(target);
        this.map = map;
    }
};

export default MapComponent;
