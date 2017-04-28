import template from './toolbar.html!text';

const ToolbarComponent = {
    template: template,
    controller: function ($http, appConfig) {
        this.appConfig = appConfig;
        this.user = appConfig.user;
        this.totalSquareFootage = null;
        $http.get('/_/locations/square-footage').then((response) => {
            this.totalSquareFootage = response.data.total;
        });
    }
};

export default ToolbarComponent;
