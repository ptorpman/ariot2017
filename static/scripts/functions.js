(function(){
	function callDataApi(){
		$.ajax({
			url: "/api_data",
			type: "GET",
			success: function(){

			}

		})
	}

	$(document).ready(function(){
		callDataApi();
	});
})();
