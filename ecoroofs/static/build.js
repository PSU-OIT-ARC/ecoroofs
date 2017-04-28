// Build JavaScript apps into bundles for production.
// Run with Node.js: `node build.js`
// Or use the ARCTasks wrapper: `inv build_js`
const path = require('path');
const Builder = require('systemjs-builder');

const baseURL = __dirname;

// APP_CONFIG needs to be set before the Builder is created.
global.APP_CONFIG = {
    baseURL: baseURL
};

// A list of our apps, relative to the static directory.
const apps = ['app'];

// Apps are traced to get dependencies trees.
const traces = [];

const configFile = path.join(baseURL, 'systemjs.config.js');
const builder = new Builder(baseURL, configFile);
const bundleOutputDir = path.join(baseURL, 'bundles');
const bundleOptions = {
    mangle: false,  // Only relevant when minify == true
    minify: true,
    runtime: false,
    sourceMaps: true
};
const globalDeps = {
    'angular/index.js': 'angular',
    'angular-material/index.js': 'null',
    'angular-resource/index.js': 'null',
    'angular-route/index.js': 'null',
    'ol/ol.js': 'ol',
    'DEBUG': false
};

console.log('Building SystemJS bundles in', baseURL);

builder.config({
    meta: {
        'angular-resource/angular-resource.js': {
            deps: ['angular']
        },
        'angular-route/angular-route.js': {
            deps: ['angular']
        },
        'ol/ol.js': {
            // Ignore OpenLayers entirely when building. This keeps it
            // from being traced for dependencies and from being
            // included in bundles.
            build: false
        }
    }
});

// Trace each app to get a tree of its dependencies.
apps.forEach((name) => {
    const main = path.join(name, 'main.js');
    console.log('Tracing app', name, 'from', main);
    traces.push(builder.trace(main))
});

// First, create a bundle containing the common Angular dependencies
// across all apps. Then, create a bundle for each app.
Promise.all(traces).then((trees) => {
    let commonTree;
    const angularBundleName = 'angular.bundle.js';
    const angularBundlePath = path.join(bundleOutputDir, angularBundleName);

    if (Object.keys(trees).length > 1) {
        commonTree = builder.intersectTrees.apply(this, trees);
    } else {
        commonTree = trees[0];
    }

    let angularTree = {};
    let angularPackages = [];
    Object.keys(commonTree).forEach((p) => {
        const parts = path.parse(p);
        const packageName = path.basename(parts.dir);
        if (parts.dir.startsWith('node_modules/angular')) {
            angularTree[p] = commonTree[p];
            angularPackages.push(packageName);
        }
    });

    console.log('Creating', path.relative(baseURL, angularBundlePath), 'with all Angular packages');
    const angularBundlePromise = builder.buildStatic(angularTree, angularBundlePath, bundleOptions);

    angularBundlePromise.then(() => {
        let bundlePromises = [];
        bundleOptions.globalDeps = globalDeps;
        apps.forEach((name, i) => {
            const tree = trees[i];
            const bundleTree = builder.subtractTrees(tree, angularTree);
            const main = path.join(name, 'main.js');
            const bundleName = [name, 'bundle', 'js'].join('.');
            const bundlePath = path.join(bundleOutputDir, bundleName);
            const relbundlePath = path.relative(baseURL, bundlePath);
            console.log('Creating', relbundlePath, 'for app', name, 'from', main);
            bundlePromises.push(builder.buildStatic(bundleTree, bundlePath, bundleOptions));
        });
        Promise.all(bundlePromises).catch((e) => console.log(e));
    });

    angularBundlePromise.catch((e) => console.error(e));
}).catch((e) => {
    console.error(e);
    process.exit(1);
});
