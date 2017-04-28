import ol from 'ol';
import template from './info.html!text';

const ContentComponent = {
    template: template,
    controller: function ($mdSidenav, map, Location) {
        const mapView = map.getView();
        const sidenavId = 'sidenav-map-info';

        // TODO: Use the current width of the sidenav instead of hard
        // TODO: coding this. Not sure of the best way to do this since
        // TODO: it's not easy to get the width of a sidenav.
        const width = 400;
        const buffer = 20;
        const bufferedWidth = width + buffer;

        this.location = null;

        // Open the right info panel. If necessary, also pan the map to
        // the left to keep the clicked point (the "anchor point") from
        // being covered by the info panel. At the same time, also make
        // sure the anchor point isn't pushed off screen. On small
        // screens, if these rules conflict, the anchor point will be
        // covered.
        this.open = (anchorPoint) => {
            const sidenav = $mdSidenav(sidenavId);

            if (sidenav.isOpen()) {
                return;
            }

            sidenav.open();

            const anchorPointX = anchorPoint[0];
            const mapWidth = map.getSize()[0];

            // Only pan if:
            //   - Opening the right sidenav *would* cover the clicked point
            //   - Panning would *not* push the clicked point off screen (to the left)
            const doPan = (anchorPointX > (mapWidth - bufferedWidth)) && (anchorPointX > bufferedWidth);

            if (doPan) {
                const center = mapView.getCenter();
                const centerPixel = map.getPixelFromCoordinate(center);
                const x = centerPixel[0];
                const y = centerPixel[1];
                const newX = x + bufferedWidth;
                const newCenter = map.getCoordinateFromPixel([newX, y]);
                mapView.animate({
                  center: mapView.getCenter(),
                  duration: 200
                });
                mapView.setCenter(newCenter);
            }
        };

        // When the info panel is closed, we intentionally don't pan
        // because trying to figure out where we should pan back to
        // isn't entirely clear, and it doesn't seem necessary for UX
        // reasons (i.e., maintaining the current map view seems fine).
        this.close = (anchorPoint) => {
            const sidenav = $mdSidenav(sidenavId);
            sidenav.close();
            map.clearHighlightOverlay();
        };

        this.showLocation = (location) => {
            const point = location.point_obscured;
            map.setCenter([point.x, point.y]);
        }

        map.on('singleclick', (event) => {
            const pixel = event.pixel;
            const feature = map.forEachFeatureAtPixel(pixel, (feature) => feature);
            if (feature) {
                const id = feature.get('id');
                this.location = Location.get({
                    id: id
                }, () => {
                    this.open(pixel);
                    map.clearHighlightOverlay();
                    map.highlightFeature(feature);
                }, () => {
                    this.close(pixel);
                });
            } else {
                this.close(pixel);
            }
        });
    }
};

export default ContentComponent;
