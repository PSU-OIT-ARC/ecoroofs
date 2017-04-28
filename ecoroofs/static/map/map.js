import ol from 'ol';

const minResolution = 0.29858214173896974;

// Use the same resolution for all GetFeatureInfo requests so feature
// outlines don't look wonky when zooming in and out. We don't use the
// minimum resolution so the returned geometry isn't too complex (which
// can seriously bog down the browser).
const getFeatureInfoResolution = minResolution * Math.pow(2, 5);

const pointRadius = 6;

const projectionCode = 'EPSG:3857';
const geographicProjectionCode = 'EPSG:4326';
const projection = ol.proj.get(projectionCode);
const geographicProjection = ol.proj.get(geographicProjectionCode);

const geojsonFormat = new ol.format.GeoJSON({
    defaultDataProjection: geographicProjection
});

const psuGreen = '#6a7f10';
const psuGreenRGB = '106,127,16';

export default class Map extends ol.Map {
    constructor ($http, appConfig) {
        const options = appConfig.map;

        const center = ol.proj.fromLonLat(options.view.center);
        const serverOptions = options.server;
        const mapServerBaseURL = serverOptions.baseURL;
        const workspace = serverOptions.workspace;

        const neighborhoodLayerBreakpoint = minResolution * Math.pow(2, 3);
        const neighborhoodLayerMaxResolution = minResolution * Math.pow(2, 11);
        const neighborhoodLayer = makeWMSLayer(mapServerBaseURL, workspace, 'neighborhoods', {
            label: 'Neighborhoods',
            minResolution: neighborhoodLayerBreakpoint,
            maxResolution: neighborhoodLayerMaxResolution,
            opacity: 0.4
        });

        const neighborhoodLayerMax = makeWMSLayer(mapServerBaseURL, workspace, 'neighborhoods', {
            label: 'Neighborhoods',
            maxResolution: neighborhoodLayerBreakpoint,
            opacity: 0.2,
            source: neighborhoodLayer.getSource()
        });

        const neighborhoodHighlightLayerMinResolution = minResolution * Math.pow(2, 4);
        const neighborhoodHighlightSource = new ol.source.Vector();
        const neighborhoodHighlightLayer = new ol.layer.Vector({
            minResolution: neighborhoodHighlightLayerMinResolution,
            maxResolution: neighborhoodLayerMaxResolution,
            source: neighborhoodHighlightSource,
            style: new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: 'white',
                    width: 2
                }),
                fill: new ol.style.Fill({
                    color: `rgba(${psuGreenRGB}, 0.25)`
                })
            })
        });

        const baseLayers = [
            new ol.layer.Tile({
                label: 'Road Map',
                shortLabel: 'Map',
                source: new ol.source.BingMaps({
                    key: options.bing.key,
                    imagerySet: 'Road'
                })
            })
        ];

        const wmsLayers = [
            neighborhoodLayer,
            neighborhoodLayerMax
        ];

        const wmsHighlightLayers = [
            neighborhoodHighlightLayer
        ];

        const featureLayers = [
            makeFeatureLayer(mapServerBaseURL, workspace, 'locations', 'Locations')
        ];

        const highlightOverlay = new ol.layer.Vector({
            source: new ol.source.Vector({
                features: new ol.Collection()
            }),
            style: new ol.style.Style({
                image: new ol.style.Circle({
                    radius: pointRadius + 2,
                    stroke: new ol.style.Stroke({
                        color: 'white',
                        width: 2
                    }),
                    fill: new ol.style.Fill({
                        color: 'red'
                    })
                })
            })
        });

        const searchResultsOverlay = new ol.layer.Vector({
            source: new ol.source.Vector({
                features: new ol.Collection()
            }),
            style: new ol.style.Style({
                image: new ol.style.Circle({
                    radius: 4,
                    fill: new ol.style.Fill({
                        color: '#dc9b32'
                    })
                })
            })
        });

        const overlays = [
            highlightOverlay,
            searchResultsOverlay
        ];

        const allLayers = [].concat(
            baseLayers, wmsLayers, wmsHighlightLayers, featureLayers, overlays);

        const view = new ol.View({
            center: center,
            minZoom: options.view.minZoom,
            maxZoom: options.view.maxZoom,
            zoom: options.view.zoom
        });

        super({
            layers: allLayers,
            view: view
        });

        this.$http = $http;
        this.mapServerBaseURL = mapServerBaseURL;
        this.workspace = workspace;
        this.neighborhoodSource = neighborhoodLayer.getSource();
        this.neighborhoodHighlightSource = neighborhoodHighlightSource;
        this.neighborhoodHighlightLayer = neighborhoodHighlightLayer;
        this.highlightOverlay = highlightOverlay;
        this.searchResultsOverlay = searchResultsOverlay;

        this.on('singleclick', (event) => {
            const coordinate = this.getCoordinateFromPixel(event.pixel)
            this.highlightNeighborhood(coordinate);
        });
    }

    setCenter (center, native /* =false */) {
        if (!native) {
            center = ol.proj.fromLonLat(center);
        }
        this.getView().setCenter(center);
    }

    highlightFeature (feature) {
        this.highlightOverlay.getSource().addFeature(feature);
    }

    clearHighlightOverlay () {
        this.highlightOverlay.getSource().clear(true);
    }

    highlightNeighborhood (coordinate) {
        this.highlightNeighborhoodAt(coordinate);
        // Show neighborhood info... somewhere (but not in a popup)
    }

    highlightNeighborhoodAt (coordinate) {
        const wmsSource = this.neighborhoodSource;
        const featureSource = this.neighborhoodHighlightSource;
        const url = wmsSource.getGetFeatureInfoUrl(
            coordinate, getFeatureInfoResolution, projection, {
            INFO_FORMAT: 'application/json'
        });
        return this.$http.get(url).success((data) => {
            let featureCollection = data;
            let features = featureCollection.features;
            featureSource.clear(true);
            if (features && features.length) {
                features = geojsonFormat.readFeatures(featureCollection, {
                    dataProjection: geographicProjection,
                    featureProjection: projection
                });
                featureSource.addFeatures(features);
            } else {

            }
        });
    }
}

function makeWMSLayer (baseURL, workspace, layerName, options=null) {
    options = options || {};
    options.source = options.source || new ol.source.TileWMS({
        url: [baseURL, 'wms', workspace].join('/'),
        serverType: 'geoserver',
        params: {
            LAYERS: `${workspace}:${layerName}`
        }
    });
    return new ol.layer.Tile(options);
}

function makeFeatureLayer (baseURL, workspace, layerName, label, style=null) {
    const url = `${baseURL}/wfs`;
    const baseParams = [
        'service=WFS',
        'version=2.0.0',
        'request=GetFeature',
        `typeNames=${workspace}:${layerName}`,
        `srsName=${projectionCode}`,
        'outputFormat=application/json'
    ].join('&');
    return new ol.layer.Vector({
        label: label,
        source: new ol.source.Vector({
            format: new ol.format.GeoJSON(),
            strategy: ol.loadingstrategy.bbox,
            url: function (extent) {
                const bboxParam = `${extent.join(',')},${projectionCode}`;
                const requestParams = `${baseParams}&bbox=${bboxParam}`;
                return `${url}?${requestParams}`;
            }
        }),
        style: style || new ol.style.Style({
            image: new ol.style.Circle({
                radius: pointRadius,
                stroke: new ol.style.Stroke({
                    color: '#ffffff',
                    width: 2
                }),
                fill: new ol.style.Fill({
                    color: psuGreen
                })
            })
        })
    })
}
