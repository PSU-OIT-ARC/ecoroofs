import 'angular-resource';

export default function pageResourceFactory ($resource) {
    const url = '/_/pages/:slug';
    const Page = $resource(url);
    return Page;
}
