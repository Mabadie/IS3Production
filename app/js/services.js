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

        //confirmar solicitud de libro
        dataFactory.bookrequestConfirm = function (req) {
            return $http.post(urlBase + '/book-request-confirm/',req);
        };

        //entrega  de libro
        dataFactory.bookrequestDeliver = function (req) {
            return $http.post(urlBase + '/book-request-deliver/',req);
        };

        //confirmacion de entrega de libro
        dataFactory.bookrequestConfirmDelivered = function (req) {
            return $http.post(urlBase + '/book-request-confirm-delivered/',req);
        };

	//devolucion de libro
        dataFactory.bookrequestReturn = function (req) {
            return $http.post(urlBase + '/book-request-return/',req);
        };

	//confirmacion de devolucion de libro
        dataFactory.bookrequestConfirmReturned = function (req) {
            return $http.post(urlBase + '/book-request-confirm-returned/',req);
        };

	//rechazo de solicitud de libro
        dataFactory.bookrequestReject = function (req) {
            return $http.post(urlBase + '/book-request-reject/',req);
        };

	//lista de solicitudes realizadas y recibidas
	dataFactory.myrequests= function(req){
		return $http.get(urlBase + '/book-request/',req);
	};

	//notificaciones
	dataFactory.mynotifications= function(){
                return $http.get(urlBase + '/notifications/');
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

    dataFactory.editBook = function(request){
	    return $http.post(urlBase + '/my-books/update/', request);
    }

     dataFactory.deleteBook = function(request){
	    return $http.post(urlBase + '/my-books/delete/', request);
    }
        return dataFactory;

    }]);
