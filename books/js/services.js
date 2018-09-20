'use strict';
angular.module('SHAREBOOKSApp')
    .factory('dataFactory',['$http', 'APP_CONFIG', function ($http, APP_CONFIG) {

       $http.defaults.headers.common['Content-Type'] = 'application/json';

        var urlBase = APP_CONFIG.ct_urlService +  APP_CONFIG.ct_urlBase;
        var dataFactory = {};

		//*** Auth provider service
		dataFactory.authprovider = function (ctrl) {
				return $http.get(urlBase + '/Auth-Provider/resource/'+ ctrl);
        };

        //*** Login del Usuario
        dataFactory.login = function (user) {
            return $http.post(urlBase + '/login',user);
        };

        dataFactory.formatDate = function (dateString) {

            var year        = dateString.substring(0,4);
            var month       = dateString.substring(4,6);
            var day         = dateString.substring(6,8);
            return day + '/' + month +'/'+ year;

        };
        return dataFactory;
    }]);
