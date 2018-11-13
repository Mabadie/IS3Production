'use strict';
angular.module('SHAREBOOKSApp')
    .factory('dataFactory',['$http', 'APP_CONFIG', function ($http, APP_CONFIG) {

       $http.defaults.headers.common['Content-Type'] = 'application/json';

        var urlBase = APP_CONFIG.ct_urlService + APP_CONFIG.ct_urlBase;
        var dataFactory = {};

	//*** Auth provider service
	    dataFactory.authprovider = function (ctrl) {
		return $http.get(urlBase + '/Auth-Provider/resource/'+ ctrl);
        };

        //*** Login del Usuario
        dataFactory.login = function (user) {
            return $http.post(urlBase + '/login/',user);
        };

        //*** Signup del Usuario
        dataFactory.signup = function (user) {
            return $http.post(urlBase + '/signup/',user);
        };

	    dataFactory.logout = function (user) {
            return $http.post(urlBase + '/logout/',user);
        };

	 //*** Listado de libros
        dataFactory.books = function (key) {
	    var search=(key)? "?search="+key:"";	
            return $http.get(urlBase + '/books/'+search);
        };

	//*** Listado de mis libros
	dataFactory.mybooks = function () {
            return $http.get(urlBase + '/my-books/');
        };


	//solicitud de libro
	dataFactory.bookrequest = function (req) {
            return $http.post(urlBase + '/book-request/',req);
        };

	dataFactory.myrequests= function(req){
		return $http.get(urlBase + '/book-request/',req);
	};

	dataFactory.getUser = function(userId){
	    return $http.post(urlBase + '/getUser/',userId);
    }

    dataFactory.updateUser = function(request){
	    return $http.put(urlBase +'/getUser/', request);
    }

    dataFactory.createBook = function(request){
	    return $http.post(urlBase + '/my-books/insert/',request);
    }

        return dataFactory;

    }]);
