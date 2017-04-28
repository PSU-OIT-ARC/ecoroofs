import 'angular-resource';

export default function locationResourceFactory ($resource) {
    const url = '/_/locations/:id';
    const Location = $resource(url, null, {
        search: {
            method: 'GET',
            url: '/_/locations/search/',
            isArray: true
        }
    });
    return Location;
}
