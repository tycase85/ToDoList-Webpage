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
//********************************///
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
//********************************//
		//check for session
		$scope.getLogin = function() {
			var url = 'https://info3103.cs.unb.ca:52799/signin';

			$http.get(url).success( function(response) { //success
				session['exists'] = true
				session['username'] = response.data.username
			},
			function(response) {
				session['exists'] = false
				session['username'] = null
			}
		);
	}


////////////////////////////////////////////////////////////////////////////////////////////
//not sure how to to do this one
	//GET ALL LISTS
	//checks the what the user is and returns all the list if any
	$scope.getlists = function(e, input) {
		var url = 'https://info3103.cs.unb.ca:52799/lists'; //get all lists
		$http.get(url).success( function(response) { //success
//Do stomething
// not sure
		}
	);
	}

//********************************///

	//POST A NEW LIST
	$scope.postlists = function() {
		var url = 'https://info3103.cs.unb.ca:52799/lists';
		var input = {
			//keep checking seeion for which user it is
			postedBy: session['username'],
			//what is the text box called
			listName:$('#listName').val(),
		}
		var data = JSON.stringify(dat);
		var postlist = "";

		$http({ method: 'POST', url: url, data: data }).then(
		 function(response) { //success
			 if (response.status == 200) {
				$scope.getlists(dat.listName);
				$scope.postMessage = "Post was Successful"; //this works
				console.log(session['username']);
				//what is the html
				document.getElementById("postlistItem").reset();
			 }
			 if (response.status == 401) {
				$scope.postMessage = "Unauthorized: Please Log in ";
			 }
		 }
		);
	}

//////////////////////////////////////////////////////////////////////////////////////////////

	//GET A LISTS
	//checks the what the user is and returns a list if it exist
	$scope.getlists = function(id) {
		var url = 'https://info3103.cs.unb.ca:52799/lists' + id; //get a lists
		$http.get(url).success( function(response) { //success
			listID = response
			$scope.reviews = listID


		});
	}
//********************************///

	//POST A NEW ITEM TO {listID}
$scope.postlists = function() {
	var url = 'https://info3103.cs.unb.ca:52799/lists'+ id; //get all lists
	var input = {
		//keep checking seeion for which user it is
		postedBy: session['username'],
		//what is the text box called
		itemName:$('#itemName').val(),
	}

	var data = JSON.stringify(dat);
	var postlist = "";

	$http({ method: 'POST', url: url, data: data }).then(
	 function(response) { //success
		 if (response.status == 200) {
			$scope.getlists(dat.listID);
			$scope.postMessage = "Post was Successful"; //this works
			console.log(session['username']);
			//what is the html
			document.getElementById("postlistItem").reset();
		 }
		 if (response.status == 401) {
			$scope.postMessage = "Unauthorized";
		 }
	 }
	);
}
//********************************///
//DELETE A LIST {listID}
$scope.deleteItem = function(L_id) {
	var url = "https://info3103.cs.unb.ca:52799/lists/" + id;
	var templistID = $scope.reviews[1].listID;

	$http({ method: 'DELETE', url: url}).then(
		function(response) { //success
			if (response.status == 200){
				$scope.getlists(templistID);
			}
		},
		function(response) { //error
			if (response.status == 401){}
		});
}

///////////////////////////////////////////////////////////////////////////////////////////////

	//DELETE AN ITEM {itemName}
	$scope.deleteItem = function(L_id,I_id) {
		var url = "https://info3103.cs.unb.ca:52799/lists/" + id/ + id;
		var templistID = $scope.reviews[1].listID;
		var tempitemID = $scope.reviews[2].itemID;

		$http({ method: 'DELETE', url: url}).then(
			function(response) { //success
				if (response.status == 200){
					$scope.getlists(templistID);
				}
			},
			function(response) { //error
				if (response.status == 401){}
			});
	}


}]);
