import angular from 'angular';

export default function run ($rootScope, $http, $timeout) {
    const activityEl = angular.element(document.getElementById('activity-indicator'));
    $rootScope.$watch(function () {
        return $http.pendingRequests.length;
    }, function (newLength, oldLength) {
        if (newLength > 0) {
            activityEl.removeClass('invisible');
        } else {
            $timeout(function () {
                activityEl.addClass('invisible');
            }, 500);
        }
    });
}

