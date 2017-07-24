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

        // Filters
        this.showFilters = false;
        this.usage = { id: null };
        this.depth = {
            min: null,
            max: null
        };
        this.year_built = {
            min: null,
            max: null
        }
        this.filterData =  Location.building_uses((uses) => {
            const numResults = uses.length;
            let options = [];
            if (numResults) {
                let option = {};
                uses.forEach( (use)=> {
                    option.id = use.id;
                    option.name = use.name;
                    options.push(option);
                });
                return options;
            }
        })



        this.search = () => {
            const usage = this.usage;
            const depthMin = this.depth.min;
            const depthMax = this.depth.max;
            const yearMin = this.year_built.min;
            const yearMax = this.year_built.max;
            let term = this.searchTerm;
            if (term) {
                term.replace(/^\s+|\s+$/g);
            }
            const searchFields = [term, usage, depthMin, depthMax, yearMin, yearMax];
            const shouldSearch = searchFields.filter(
                (field) => {
                    return field;
                });
            if (!shouldSearch.length) {
                return;
            }

            mapSource.clear(true);

            this.locations = Location.search({
                q: term,
                usage: usage,
                depth_min: depthMin,
                depth_max:depthMax,
                year_built_min: yearMin,
                year_built_max: yearMax
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
            this.depth.min = null;
            this.depth.max = null;
            this.usage = null;
            this.year_built.min = null;
            this.year_built.max = null;
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
