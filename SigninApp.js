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
					$scope.username = user.username;
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
	$scope.getlists = function(){
		var url = 'https://info3103.cs.unb.ca:52799/lists'; //get all lists
		$http.get(url).success( function(response) { //success
			$scope.listR = response;
			console.log(response);
			var results = [];
			var i = 0;
			var total = 5;
			for( i in response){
				//results.push(response[i]);
				console.log(response[i].listName);
				$scope.lists = response[i].listName;
				console.log($scope.lists);
				i++;
			}

			for(i=0;i<total;i++){
				$scope.allLists = response[i].listName;
			}
			//lists = {results};
			//$scope.lists = response.listName;
			//console.log(response.listName)
		});

		// $http.get(url).success( function(response) { //success
		// 	var list = 0;
		// 	var results = []
		// 	for ( list in response){
		// 		results.push(response[list].id);
		// 		list++;
		// 		console.log(list);
		// 		console.log(response[list]);
		// 	}
    //   $scope.search_results = results;
    // })

}
//////////////////////////////////////////////////////////////////////////////////

$scope.getitems = function(id){
	var url = 'https://info3103.cs.unb.ca:52799/lists/'+id; //get all lists
	$http.get(url).success( function(response) { //success
		console.log(response);
		$scope.itemR = response;
		var results = [];
		var i = 0;
		var total = 5;

		for(i=0;i<total;i++){
			$scope.allItems = response[i].listName;
		}
	});


}




//********************************///
// WORKING JUST NEED IT TO DISPLAY ON UI
	//POST A NEW LIST
	$scope.postlists = function() {
		var url = 'https://info3103.cs.unb.ca:52799/lists';
		var input = {
			//what is the text box called
			listName:$('#addlist').val(),
		}
		var data = JSON.stringify(input);
		var postlist = "";

		$http({ method: 'POST', url: url, data: data }).then(
		 function(response) { //success
			 if (response.status == 200) {
				$scope.getlists(data.listName);
				$scope.postMessage = "Post was Successful"; //this works

				$scope.addlist = null
			 }
			 if (response.status == 401) {
				$scope.postMessage = "Unauthorized: Please Log in ";
			 }
		 }
		);
	}


	//POST A NEW ITEM TO {listID}
$scope.postitem = function(id) {
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
			$scope.postitem(dat.itemID);
			$scope.postMessage = "Post was Successful"; //this works

			$scope.additem = null
		 }
		 if (response.status == 401) {
			$scope.postMessage = "Unauthorized";
		 }
	 }
	);
}
// //********************************///
// //DELETE A LIST {listID}
$scope.deleteItem = function(L_id) {
	var url = "https://info3103.cs.unb.ca:52799/lists/" + id;
	var templistID = $scope.list.listName;

	$http({ method: 'DELETE', url: url}).then(
		function(response) { //success
			if (response.status == 200){
				$scope.list(L_id).splice(index, 1);
				$scope.getlists(templistID);
			}
		},
		function(response) { //error
			if (response.status == 401){}
		});
}



}]);
