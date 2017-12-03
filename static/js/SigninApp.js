angular.module('SigninApp', [])
  .controller('SigninController', ['$scope', '$http', function($scope, $http) {
    $scope.isLoggedIn = false;

    $scope.signin = function (user){
      credentials = JSON.stringify({"username": user.username, "password": user.password});

	   // Submit the credentials
     $http.post('https://info3103.cs.unb.ca:52799/signin', credentials ).then(function(data) {
        // Success here means the transmission was successful - not necessarily the login.
        // The data.status determines login success
        if(data.status == 201) {
          console.log("Accepted Login");
          $scope.isLoggedIn = true;
          // You're in!
          // But does the session carry? Let's try some other endpoint that requires a login
           $http.get('https://info3103.cs.unb.ca:52799/lists').then( function(data){
                           $scope.message = data.data.message;
            });
       }
    });
  }

    //logout user
  $scope.logout = function() {
    var url = 'https://info3103.cs.unb.ca:52799/signin'

    $http({ method: 'DELETE', url: url }).then(
      function(response) { //success
        if (response.status == 200) {
          $scope.isLoggedIn = false;
          session['exists'] = false
          session['username'] = null
        }
      }
    );
  }

}]);
