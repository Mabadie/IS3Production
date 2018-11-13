'use strict';
angular.module('SHAREBOOKSApp')
    .controller('RootCtrl', ['$scope','$rootScope','$routeParams', '$location','dataFactory','$window','$http',
        function ($scope, $rootScope, $routeParams,  $location, dataFactory, $window, $http) {
			
	    $rootScope.usuario={"logged_in":false,id:null};
            $rootScope.status={"hayerror":false,"success":false,"msg":null};
	    $rootScope.esLogout=false;
            $scope.status.hayerrorLogin=false;
            $rootScope.ajaxCount=0;
	    $rootScope.notifications=[];
	    $rootScope.interval=null;	 		   
	    $rootScope.notifCount="";
	
            $('nav').addClass('shrink');
	    $(".nav a").on("click", function(){
            	$(".nav").find(".active").removeClass("active");
   		$(this).parent().addClass("active");
	    });		

	    $location.path("/login");

            $rootScope.cerrarModal=function(modDiag){
                $(modDiag).modal('toggle');
            };

            $rootScope.logout=function(){
		$rootScope.esLogout=true;
                dataFactory.logout($rootScope.usuario.nroCliente)
                    .success(function(data,status){
                            $rootScope.usuario.logged_in=false;
			    $rootScope.stopNotifications();	
			    $http.defaults.headers.common['Authorization']="";	
                            $location.path("/login");
                 });
            }

	$rootScope.formatDate = function (dateString) {
	    
            if(!dateString) return;	
            var year        = dateString.substring(0,4);
            var month       = dateString.substring(5,7);
            var day         = dateString.substring(8,10);
            return day + '/' + month +'/'+ year;

        };

        $rootScope.formatState = function (state) {

                switch(state)
                {
                        case(0): return "Solicitud Enviada";
                        case(1): return "Solicitud Aceptada";
                        case(2): return "Entregado-No confirmado";
			case(3): return "Entregado";
                        case(4): return "Devuelto-No confirmado";
			case(5): return "Devuelto";
                        case(6): return "Solicitud Rechazada";
                }
        };

	$rootScope.startNotifications=function()
	{
		$rootScope.interval=setInterval(function(){
			dataFactory.mynotifications().success(function(data)
			{
				var count=0;
				for(var n in $rootScope.notifications){ 
					if(!$rootScope.notifications[n].done) count++;
				}

				$rootScope.notifCount=(count==0)?"":count;
				$rootScope.notifications=data;
			});

		},3000);	
	}

	$rootScope.stopNotifications=function()
        {
                clearInterval($rootScope.interval)
        }


    }]);


angular.module('SHAREBOOKSApp')
    .controller('LoginCtrl', ['$scope','$rootScope','$routeParams', '$location','$http', 'dataFactory',
        function ($scope, $rootScope, $routeParams,  $location, $http, dataFactory) {
            $rootScope.status = {"hayerror": false, "success": false, "msg": null};
            $rootScope.esLogout=false;
            $scope.loginUsr = {'username': null, 'password': null};
	    $scope.signupUsr = {'username': null, 'password': null,'rpassword': null, 'email':null}	

	    $scope.login=function()
	    {
       		var cliente = {'username': $scope.loginUsr.username, 'password': $scope.loginUsr.password};

            	dataFactory.login(cliente).error(function (error, status){
                        $scope.status.msgLogin = "Datos no validos";
       	               	$scope.status.hayerrorLogin = true;
               	}).success(function (data, status) {

			if (status == 200)
			{
                        	$http.defaults.headers.common['Authorization'] = "Token "+data.token;
		                $rootScope.usuario.logged_in=true;
				$rootScope.usuario.id=data.id;
				$rootScope.startNotifications();
                 		$location.url("/books");
                    	}
                 });


             }
	  
	    $scope.signup=function()
	    {
		var usuario = {'username': $scope.signupUsr.username, 'password': $scope.signupUsr.password,
				'rpassword': $scope.signupUsr.rpassword, 'email': $scope.signupUsr.email};

            	dataFactory.signup(usuario).error(function (error, status){
                        $scope.status.msgLogin = "Datos no validos";
       	               	$scope.status.hayerrorLogin = true;
               	}).success(function (data, status) {

			if (status == 200)
			{
				$http.defaults.headers.common['Authorization'] = "Token "+data.token;
                                $rootScope.usuario.logged_in=true;
				$rootScope.usuario.id=data.id;
                                $location.url("/books");
                    	}
                 });


             }


}]);

		

angular.module('SHAREBOOKSApp')
    .controller('BooksCtrl', ['$scope','$rootScope','$routeParams', '$location','$window','dataFactory','modalService',
        function ($scope, $rootScope, $routeParams,  $location, $window, dataFactory,modalService) {
           $rootScope.status={"hayerror":false,"success":false,"msg":null};
	   $scope.search_txt="";		   
	
	   dataFactory.books().success(function(data)
	   {
		$scope.books=data;	
           });
			
			
           $scope.bookRequest=function(book)
	   {
			
			var modalOptions = {
                		mType:'confirm',
                		closeButtonText: 'Cancelar',
                		actionButtonText: 'Solicitar',
                		headerText: 'Solicitar libro',
                		bodyText: 'Desea enviar una solicitud para "'+book.title+'"?'
               		};
			
			 modalService.showModal({}, modalOptions).then(function (result) {
						
				var req={'book':book.id};
				dataFactory.bookrequest(req).success(function(data)
				{
					
					
					


				});	

			 });
	}
	  
       $scope.search=function()
       {
		dataFactory.books($scope.search_txt).success(function(data)
	        {
                	$scope.books=data;
           	});
       }

}]);





angular.module('SHAREBOOKSApp')
    .controller('MyBooksCtrl', ['$scope','$rootScope','$routeParams', '$location','$http', 'dataFactory','modalService',
    function ($scope, $rootScope, $routeParams,  $location, $http, dataFactory, modalService)
	{
			$rootScope.status={"hayerror":false,"success":false,"msg":null};
			$scope.book={title:'',author:'',year:'',image:'img/book.jpg'};

			dataFactory.mybooks().success(function(data)
                	{
				$scope.books=data;				
	                });					
			
			
				$scope.delete=function(book)
				{
					 var modalOptions = {
                				mType:'confirm',
				                closeButtonText: 'Cancelar',
				                actionButtonText: 'Borrar',	
				                headerText: 'Borrar libro',
				                bodyText: 'Desea borrar "'+book.title+'"?'
              				};

                	         	modalService.showModal({}, modalOptions).then(function (result){
		
		        	        });				
				}				

				$scope.edit=function(book)
				{
					$scope.book=book;
					$('#editBookModal').modal('toggle');
				}

				$scope.new=function()
				{
                                        $('#newBookModal').modal('toggle');
				}

				$scope.editBook=function()
				{
					alert('submit changes')				
				}

				$scope.imageChange=function()
				{
					alert('image changes')
				}

}]);





angular.module('SHAREBOOKSApp')
    .controller('NotificationsCtrl', ['$scope','$rootScope','$routeParams', '$location','$http', 'dataFactory','modalService',
    function ($scope, $rootScope, $routeParams,  $location, $http, dataFactory, modalService)
    {
                $rootScope.status={"hayerror":false,"success":false,"msg":null};

                /*$scope.notifications=
                [
                        {type:'alert-info',title:'Calificacion',body:'Te han calificado con 5 estrellas!!',link:'#'},
                        {type:'alert-warning',title:'Solicitud',body:'Tienes una solicitud pendiente',link:'#'},
			{type:'alert-success',title:'Solicitud',body:'Tu solicitud se realizo correctamente',link:''}
                ];*/

}]);



angular.module('SHAREBOOKSApp')
    .controller('SharedCtrl', ['$scope','$rootScope','$routeParams', '$location','$http', 'dataFactory','modalService',
    function ($scope, $rootScope, $routeParams,  $location, $http, dataFactory, modalService)
    {
                $rootScope.status={"hayerror":false,"success":false,"msg":null};
		$scope.concedidos=[];
		$scope.recibidos=[];
		$scope.request={};
                	
		dataFactory.myrequests().success(function(data)
                {

	                for(var sh in data)
        	        {
                	        if(data[sh].user==$rootScope.usuario.id)
                        	        $scope.recibidos.push(data[sh]);
	                        else
        	                        $scope.concedidos.push(data[sh]);
                	}

                });

		
		$scope.requestDetail=function(req)
		{
			$scope.request=req;
                        $('#showRequestModal').modal('toggle');			
		}
}]);
