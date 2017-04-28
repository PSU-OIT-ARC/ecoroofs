(function (global) {
    const baseURL = global.APP_CONFIG.baseURL;

    // These are dynamically added to map and packages.
    const angularPackages = [
        'angular',
        'angular-animate',
        'angular-aria',
        'angular-material',
        'angular-messages',
        'angular-resource',
        'angular-route'
    ];

    // Our local packages, which are dynamically added to packages.
    const localPackages = [
        'app',
        'config',
        'locations',
        'map',
        'pages',
        'toolbar',
    ]

    const map = {
        'ol': 'node_modules/openlayers/dist',
        'systemjs-babel-build': 'node_modules/systemjs-plugin-babel/systemjs-babel-browser.js',
        'systemjs-plugin-babel': 'node_modules/systemjs-plugin-babel/plugin-babel.js',
        'text': 'node_modules/systemjs-plugin-text/text.js'
    };

    const packages = {
        'ol': {
            main: 'ol',
            defaultExtension: 'js'
        }
    };

    // Loop vars.
    let name, i, len;

    for (i = 0, len = angularPackages.length; i < len; ++i) {
        name = angularPackages[i];
        map[name] = `node_modules/${name}`;
        packages[name] = {
            main: 'index',
            defaultExtension: 'js'
        }
    }

    for (i = 0, len = localPackages.length; i < len; ++i) {
        name = localPackages[i];
        packages[name] = {
            main: 'main',
            defaultExtension: 'js'
        }
    }

    const config = {
        baseURL: baseURL,
        map: map,
        packages: packages,
        transpiler: 'systemjs-plugin-babel'
    };

    System.config(config);
})(this);
