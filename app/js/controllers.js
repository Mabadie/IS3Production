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
                            $rootScope.logedUser = null;
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
		                $rootScope.usuario.id=data.id;
                 		$location.url("/books");
                 		var request = {'userId':$rootScope.usuario.id};
						dataFactory.getUser(request).success(function(data)
						{
							$rootScope.logedUser=data;
						});

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
                                $location.url("/books");
                    	}
                 });
            	var request = {'userId':$rootScope.usuario.id};
				dataFactory.getUser(request).success(function(data)
				{
					$rootScope.logedUser=data;
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
					
					var modalOptions2 = {
                        		mType:'notify',
                        		actionButtonText: 'Ok',
                        		bodyText: "La solicitud fue enviada con exito"
                    		};
                   		
				 modalService.showModal({}, modalOptions2)	
					


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
                	         		var request = {'id': book.id};
                	         		console.log(request);
									dataFactory.deleteBook(request);
									dataFactory.mybooks().success(function(data)
									{
										$scope.books=data;
									});
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

				$scope.newBook=function()
				{
					var reqCreateBook = {
						"owner":$rootScope.logedUser.username,
						"title":$scope.book.title,
						"year":$scope.book.year,
						"author":$scope.book.author,
						"image":$scope.book.image
					};
					dataFactory.createBook(reqCreateBook);
					dataFactory.mybooks().success(function(data)
                	{
						$scope.books=data;
	                });
					$('#newBookModal').modal('hide');
				}

				$scope.editBook=function()
				{
					var editBookRequest = {
						'id':$scope.book.id,
						'title':$scope.book.title,
						'author':$scope.book.author,
						'year':$scope.book.year,
						'image':$scope.book.image
					}
					dataFactory.editBook(editBookRequest);
					$('#editBookModal').modal('hide');
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
		$scope.request={};
		
		$scope.showDetail=function(req)
		{
			$scope.request=req;
			if(req.book.owner==$rootScope.usuario.id && req.state==0)$('#acceptRequestModal').modal('toggle');
			else
			if(req.book.owner==$rootScope.usuario.id && req.state==1)$('#deliverRequestModal').modal('toggle');
			else
			$('#showRequestModal').modal('toggle');
		}


		$scope.aceptar=function()
		{
			dataFactory.bookrequestConfirm({'id':$scope.request.id}).success(function()
			{
				$('#acceptRequestModal').modal('toggle');

				var modalOptions2 = {
                                mType:'notify',
                                actionButtonText: 'Ok',
                                bodyText: "La solicitud fue confirmada"}

				modalService.showModal({}, modalOptions2)				
	
			});

		}
		
		$scope.rechazar=function()
		{
			
			dataFactory.bookrequestReject({'id':$scope.request.id}).success(function()
                        {
				$('#acceptRequestModal').modal('toggle');		
				
                                var modalOptions2 = {
                                mType:'notify',
                                actionButtonText: 'Ok',
                                bodyText: "La solicitud fue rechazada"}

				modalService.showModal({}, modalOptions2)

                        });
						
		}

		$scope.entregar=function()
                {

                        dataFactory.bookrequestDeliver({'id':$scope.request.id}).success(function()
                        {
                                $('#deliverRequestModal').modal('toggle');

                                var modalOptions2 = {
                                mType:'notify',
                                actionButtonText: 'Ok',
                                bodyText: "Se envio la confirmacion de entrega"}

                                modalService.showModal({}, modalOptions2)

                        });

                }


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


angular.module('SHAREBOOKSApp')
    .controller('AccountCtrl', ['$scope','$rootScope','$routeParams', '$location','$http', 'dataFactory','modalService',
    function ($scope, $rootScope, $routeParams,  $location, $http, dataFactory, modalService)
    {
    	$scope.profileUsr = {'username': null,'actualPassword':null, 'password': null,'rpassword': null, 'email':null}
    	$scope.errorMsg=null;
    	$scope.showPasswordMessage = false;
    	var request = {'userId':$rootScope.usuario.id};
		dataFactory.getUser(request).success(function(data)
			{
				$scope.errorMsg=null;
				$rootScope.logedUser=data;
			}).error($scope.errorMsg="Ups, ocurrio un error al obtener los datos");


		$scope.updateNameModal=function()
		{
			$('#modifyNameModal').modal('toggle');
		}

		$scope.updateName=function()
		{
			var reqUpdateName = {'userId':$rootScope.usuario.id, 'type':'name', 'username':$scope.profileUsr.username};

			dataFactory.updateUser(reqUpdateName).success(function(response) {
                $rootScope.logedUser = response
				$scope.errorMsg = null;;
            });

			$('#modifyNameModal').modal('hide');
		}

		$scope.updateEmailModal=function()
		{
			$('#modifyEmailModal').modal('toggle');
		}

		$scope.updateEmail=function()
		{
			var reqUpdateEmail = {'userId':$rootScope.usuario.id, 'type':'email', 'email':$scope.profileUsr.email};
			dataFactory.updateUser(reqUpdateEmail).success(function(response) {
                $rootScope.logedUser = response;
                $scope.errorMsg = null;

            });
			$('#modifyEmailModal').modal('hide');
		}

		$scope.updatePasswordModal=function()
		{
			$('#modifyPasswordModal').modal('toggle');
		}

		$scope.updatePassword=function()
		{
			var reqUpdatePassword = {'userId':$rootScope.usuario.id, 'type':'password',
				'actualPassword': $scope.profileUsr.actualPassword,
				'password':$scope.profileUsr.password,
				'rpassword':$scope.profileUsr.rpassword };
			dataFactory.updateUser(reqUpdatePassword).success(function (response) {
				$scope.errorMsg = null;
				$scope.showPasswordMessage = true;
            }).error(function(error){
				console.log(error);
				if(error.status=400){
					$scope.errorMsg = error.message;
				}
			});
			$('#modifyPasswordModal').modal('hide');

		}



}]);
