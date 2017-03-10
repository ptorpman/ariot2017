(function(){
	function callDataApi(){
		$.ajax({
			url: "/api_data",
			type: "GET",
			success: function(data){
				console.log(data);
			}

		})
	}

	$(document).ready(function(){
		callDataApi();
	});
})();
