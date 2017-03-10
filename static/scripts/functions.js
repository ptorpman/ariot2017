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

	$(document).ready(function(){
		var refresher = setInterval(function(){
			callAjax('/api_data', callDataApi);
		}, 5000)
		callAjax('/api_data', callDataApi);

		$('.controlImg').click(function(){
			$(this).toggleClass('active');
		});

		$('#lampToggle').click(function(){
			if($(this).hasClass('active')){
					callAjax("/turnOffLights", function(){});
			} else {
					callAjax("/turnOnLights", function(){});
			}
		});

		$('#fanToggle').click(function(){
			if($(this).hasClass('active')){
					callAjax("/turnOffFan", function(){});
			} else {
					callAjax("/turnOnFan", function(){});
			}
		});

			$('#cameraToggle').click(function(){
					var $that = $(this);
					callAjax("/take_picture", function(){});
					setTimeout(function(){
							$that.removeClass('active');
					}, 5000);
			});
	});
})();
