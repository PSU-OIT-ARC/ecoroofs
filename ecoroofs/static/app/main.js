import angular from 'angular';
import 'angular-material';
import 'angular-resource';
import 'angular-route';
import config from './config';
import run from './run';
import Map from 'map/map';
import MapInfoComponent from 'map/info.component';
import MapSearchComponent from 'map/search.component';
import MapComponent from 'map/map.component';
import PageComponent from 'pages/page.component';
import ToolbarComponent from 'toolbar/toolbar.component';
import locationResourceFactory from 'locations/location';
import pageResourceFactory from 'pages/page';

const ecoroofsApp = angular
    .module('ecoroofsApp', [
        'ngMaterial',
        'ngResource',
        'ngRoute'
    ])
    .config(config)
    .run(run)
    .constant('appConfig', APP_CONFIG)
    .factory('Page', pageResourceFactory)
    .factory('Location', locationResourceFactory)
    .service('map', Map)
    .component('ecoroofsMap', MapComponent)
    .component('ecoroofsMapInfo', MapInfoComponent)
    .component('ecoroofsMapSearch', MapSearchComponent)
    .component('ecoroofsPage', PageComponent)
    .component('ecoroofsToolbar', ToolbarComponent)
    .component('notFound', {
        template: `
            <md-content class="standard-padding">
                <h1>Not Found</h1>
                <p>That page could not be found.</p>
            </md-content>
        `
    })

angular.bootstrap(document.body, [ecoroofsApp.name]);

export default ecoroofsApp;
