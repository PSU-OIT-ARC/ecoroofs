import template from './info.html!text';

const ContentComponent = {
    template: template,
    controller: function ($mdSidenav, map, Location) {
        const mapView = map.getView();
        const sidenavId = 'sidenav-map-info';
        const width = 320;  // XXX
        let panned = false;

        this.location = null;

        this.pan = (direction) => {
            const center = mapView.getCenter();
            const centerPixel = map.getPixelFromCoordinate(center);
            const x = centerPixel[0];
            const y = centerPixel[1];
            const newX = x + (width * direction);
            const newCenter = map.getCoordinateFromPixel([newX, y]);
            const pan = ol.animation.pan({
                source: map.getView().getCenter(),
                duration: 200
            });
            map.beforeRender(pan);
            mapView.setCenter(newCenter);
        };

        this.open = (pixel) => {
            const sidenav = $mdSidenav(sidenavId);
            const right = document.documentElement.clientWidth;
            if (!sidenav.isOpen()) {
                sidenav.open();
                if (pixel[0] - width > 0 && right - width < pixel[0]) {
                    this.pan(1, pixel);
                    panned = true;
                }
                else panned = false;
            }
        };

        this.close = (pixel) => {
            const sidenav = $mdSidenav(sidenavId);
            if (sidenav.isOpen()) {
                sidenav.close();
                if (panned) {
                    this.pan(-1, pixel);
                }
            }
        };

        map.on('singleclick', (event) => {
            const feature = map.forEachFeatureAtPixel(event.pixel, (feature) => feature);
            if (feature) {
                const slug = feature.get('slug');
                this.location = Location.get({
                    slug: slug
                }, () => {
                    this.open(event.pixel);
                }, () => {
                    this.close(event.pixel);
                });
            } else {
                this.close(event.pixel);
            }
        });
    }
};

export default ContentComponent;
