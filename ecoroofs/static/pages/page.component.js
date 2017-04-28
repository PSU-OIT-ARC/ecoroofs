const PageComponent = {
    templateUrl: '/static/pages/page.html',
    controller: function ($routeParams, Page) {
        this.page = Page.get({
            slug: $routeParams.slug
        });
    }
};

export default PageComponent;
