import ol from 'ol';
import template from './search.html!text';
import Location from 'locations/location';

const SearchComponent = {
    template: template,
    controller: function ($scope, map, Location) {
        const mapView = map.getView();
        const mapSource = map.searchResultsOverlay.getSource();

        this.locations = null;
        this.searchTerm = null;
        this.hasSearchResults = false;
        this.numSearchResults = null;
        this.searchResultsMessage = null;

        this.search = () => {
            const term = this.searchTerm.replace(/^\s+|\s+$/g);

            if (!term) {
                return;
            }

            mapSource.clear(true);

            this.locations = Location.search({
                q: term
            }, (locations) => {
                const numSearchResults = locations.length;
                const s = numSearchResults === 1 ? '' : 's';
                this.hasSearchResults = true;
                this.numSearchResults = numSearchResults;
                this.searchResultsMessage = `${numSearchResults} search result${s}`;
                if (numSearchResults) {
                    let location;
                    let coordinates;
                    let point;
                    let feature;
                    let features = [];
                    for (let i = 0; i < numSearchResults; ++i) {
                        location = locations[i];
                        coordinates = location.point_obscured;
                        coordinates = [coordinates.x, coordinates.y];
                        coordinates = ol.proj.fromLonLat(coordinates);
                        point = new ol.geom.Point(coordinates);
                        feature = new ol.Feature({
                            id: location.id,
                            name: location.name,
                            geometry: point
                        });
                        features.push(feature);
                    }
                    mapSource.addFeatures(features);
                    if (numSearchResults > 1) {
                        mapView.fit(ol.extent.buffer(mapSource.getExtent(), 500));
                    } else {
                        mapView.setCenter(coordinates);
                    }
                }
            }, () => {
                this.searchResultsMessage = 'Unable to search at this time';
            });
        }

        this.resetSearch = () => {
            this.locations = null;
            this.searchTerm = null;
            this.hasSearchResults = false;
            this.numSearchResults = null;
            this.searchResultsMessage = null;
            mapSource.clear(true);
        }

        $scope.$watch(() => {
            return this.searchTerm;
        }, (newVal) => {
            if (!newVal) {
                this.resetSearch();
            }
        })
    }
};

export default SearchComponent;
