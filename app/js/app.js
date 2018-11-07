'use strict';

var app = angular.module('SHAREBOOKSApp', ['ngRoute','ui.bootstrap']);

app.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/books', {controller: 'BooksCtrl',templateUrl: './views/books.html'});
	$routeProvider.when('/my-books', {controller: 'MyBooksCtrl',templateUrl: './views/mybooks.html'});
	$routeProvider.when('/shared', {controller: 'SharedCtrl',templateUrl: './views/shared.html'});
	$routeProvider.when('/login', {controller: 'LoginCtrl',templateUrl: './views/login.html'});
	$routeProvider.when('/register', {controller: 'LoginCtrl',templateUrl: './views/register.html'});
	$routeProvider.when('/notifications', {controller: 'NotificationsCtrl',templateUrl: './views/notifications.html'});

    	$routeProvider.otherwise({ redirectTo: '/books' });
}]);

var interceptor=function($q, $rootScope, $log) {
    return {
        'request': function(config){
            $rootScope.ajaxCount++;
            $('#loading-indicator').show();
            return config;
        },
        'response': function(result){
            $rootScope.ajaxCount--;
            if ($rootScope.ajaxCount<=0) {
                $('#loading-indicator').hide();
            }
            return result;

        },
        'responseError': function(rejection) {
            $rootScope.ajaxCount--;
            if ($rootScope.ajaxCount<=0) {
                $('#loading-indicator').hide();
            }
            switch (rejection.status) {
                case 500:
                    if (typeof rejection.data.TextoResp != "undefined") {

                        if(rejection.data.CodResp==-1){
                            if ($rootScope.esLogout){
                                break;
                            }
                            if(rejection.data.TextoResp=='No existe sesion. Debe hacer login en el sistema') {
                                $('#sesExpired').modal({"backdrop": "static", "keyboard": false});
                                break;
                            }
                        }
                        
                 	
			if(rejection.data.CodResp==300)break;

			$log.warn(rejection.status+':'+rejection.statusText + ' : Código Respuesta:' + rejection.data.CodResp + ' - ' + rejection.data.TextoResp);
                        $rootScope.status.msg = "Error: "+ rejection.data.TextoResp;
                        $rootScope.status.hayerror = true;
                    }else{
                        $log.warn(rejection.status+':'+rejection.statusText);
                        $rootScope.status.msg = rejection.statusText;
                        $rootScope.status.hayerror =true;
                    }
                    break;
                default :
		    console.log(rejection);	
                    $log.warn(rejection.status+':'+rejection.statusText);
                    $rootScope.status.msg = rejection.data;
                    $rootScope.status.hayerror =true;
                    break;
            }

            return $q.reject(rejection);
        }
    };
};

app.config(function($provide, $httpProvider) {
        $httpProvider.interceptors.push(interceptor);
    });




app.run(['$rootScope', '$location',  function ($rootScope, $location ) {
       
		$rootScope.$on("$routeChangeError",function(event, previous, current, rejection){
			 $location.path('/books');
		});

		$rootScope.$on("$routeChangeStart", function (event, next, current) {
			
            	if (!$rootScope.usuario.logged_in) 
               		if (next.$$route.originalPath != "/login" && next.$$route.originalPath != "/register") 
				$location.path('/login');
            		
        	});

}]);

app.service('modalService',  ['$modal',function ($modal) {
        var modalDefaults = {
            backdrop: true,
            keyboard: true,
            modalFade: false,
            templateUrl: './partials/modal.html'
        };

        var modalOptions = {
            closeButtonText: 'Cerrar',
            actionButtonText: 'Aceptar',
            headerText: '',
            mType:'notify',
            bodyText: 'Perform this action?'
        };

        this.showModal = function (customModalDefaults, customModalOptions) {
            if (!customModalDefaults) customModalDefaults = {};
            customModalDefaults.backdrop = 'static';
            return this.show(customModalDefaults, customModalOptions);
        };

        this.show = function (customModalDefaults, customModalOptions) {
            var tempModalDefaults = {};
            var tempModalOptions = {};

            angular.extend(tempModalDefaults, modalDefaults, customModalDefaults);
            angular.extend(tempModalOptions, modalOptions, customModalOptions);

            if (!tempModalDefaults.controller) {
                tempModalDefaults.controller = function ($scope, $modalInstance) {
                    $scope.modalOptions = tempModalOptions;
                    $scope.modalOptions.ok = function (result) {
                        $modalInstance.close(result);
                    };
                    $scope.modalOptions.close = function (result) {
                        $modalInstance.dismiss('cancel');
                    };
                }
            }
            return $modal.open(tempModalDefaults).result;
        };
    }]);

