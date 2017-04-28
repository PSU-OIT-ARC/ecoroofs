export default function config ($compileProvider, $httpProvider, $locationProvider,
                                $mdThemingProvider, $resourceProvider, $routeProvider) {
    if (!APP_CONFIG.debug) {
        // Disable debug data in production.
        // See https://docs.angularjs.org/guide/production.
        $compileProvider.debugInfoEnabled(false);
    }

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    $locationProvider.hashPrefix('!');

    $resourceProvider.defaults.stripTrailingSlashes = false;

    $routeProvider
        .when('/', {
            template: `
                <ecoroofs-map>
                    <ecoroofs-map-search></ecoroofs-map-search>
                    <ecoroofs-map-info></ecoroofs-map-info>
                </ecoroofs-map>`
        })

        .when('/pages/:slug', {
            template: '<ecoroofs-page></ecoroofs-page>'
        })

        .when('/not-found', {
            template: '<not-found></not-found>'
        })

        .otherwise('/not-found');

    $mdThemingProvider.definePalette('psuGreen', {
        '50': '#c1e42a',
        '100': '#b6da1b',
        '200': '#a3c319',
        '300': '#90ac16',
        '400': '#7d9613',
        '500': '#6A7F10',
        '600': '#57680d',
        '700': '#44520a',
        '800': '#313b07',
        '900': '#1e2405',
        'A100': '#c8e741',
        'A200': '#ceea58',
        'A400': '#d5ed6e',
        'A700': '#0b0e02',
        'contrastDefaultColor': 'light',
        'contrastDarkColors': '50 100 200 A100',
        'contrastStrongLightColors': '300 400 A200 A400'
    });

    $mdThemingProvider.definePalette('psuLightGreen', {
        '50': '#191b00',
        '100': '#313400',
        '200': '#494e00',
        '300': '#616700',
        '400': '#788100',
        '500': '#909a00',
        '600': '#c0cd00',
        '700': '#d8e700',
        '800': '#eeff01',
        '900': '#f0ff1b',
        'A100': '#c0cd00',
        'A200': '#A8B400',
        'A400': '#909a00',
        'A700': '#f1ff34',
        'contrastDefaultColor': 'dark',
        'contrastLightColors': '700 800 900',
        'contrastStrongLightColors': '700 800 900'
    });

    $mdThemingProvider.definePalette('psuRed', {
        '50': '#e9a292',
        '100': '#e5907d',
        '200': '#e17e68',
        '300': '#dc6c52',
        '400': '#d85a3d',
        '500': '#D2492A',
        '600': '#bd4226',
        '700': '#a73a22',
        '800': '#92331d',
        '900': '#7d2b19',
        'A100': '#edb4a7',
        'A200': '#f2c7bd',
        'A400': '#f6d9d2',
        'A700': '#682415',
        'contrastDefaultColor': 'light',
        'contrastDarkColors': '50 100 200 300 A100',
        'contrastStrongLightColors': '400 500 600 700 A200 A400 A700'
    });

    $mdThemingProvider.theme('default')
        .primaryPalette('psuGreen')
        .accentPalette('psuLightGreen')
        .warnPalette('psuRed')
}

