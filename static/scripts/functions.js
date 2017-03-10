(function(){

	function callAjax(url, success){
			$.ajax({
				url: url,
				type: "GET",
				success: success
			});
	}

	function callDataApi(data){
			$('#measurementTable tbody').empty();
	    $.each(data, function(i, item) {
		   	var $tr = $('<tr>').append(
	            $('<td>').text(i),
	            $('<td>').text(item)
	        ).appendTo('#measurementTable');
			})
	}

	function turnOnLights(){
			$('#lampOn').css('color', 'green');
			$('#lampOff').css('color', 'red');
			//Set button rights.
	}

	function turnOffLights(){

	}

	function setAutoLights(){

	}

	function turnOnFan(){

	}

	function turnOffFan(){

	}

	function setAutoFan(){

	}

	$(document).ready(function(){
		//var refresher = setInterval(function(){
			callAjax('/api_data', callDataApi);
		//}, 5000)
			$('#lampOn').click(function(){
				callAjax("/turnOnLights", turnOnLights);
			});

			$('#lampOff').click(function(){
				callAjax("/turnOnLights", turnOffLights);
			});
	});
})();
