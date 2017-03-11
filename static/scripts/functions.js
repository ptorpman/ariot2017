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

				if( i === "WaterAlarm") {
					switch (item){
						case "green":
							$('#waterImage').attr('src','/static/images/water_level_green_traffic.png');
							break;
						case "yellow":
							$('#waterImage').attr('src','/static/images/water_level_yellow_traffic.png');
							break;
						default:
							$('#waterImage').attr('src','/static/images/water_level_red_traffic.png');
							break;
					}
				} else if (i === "DoorOpen"){
				   	var $tr = $('<tr>').append(
			            $('<td>').text(i),
			            $('<td>').text(item ? "Ja" : "Nej")
			        ).appendTo('#measurementTable');
				} else if(item instanceof Array) {
			   	var $tr = $('<tr>').append(
		            $('<td>').text(i),
		            $('<td>').text(parseFloat(item[0]).toFixed(2) + ((i.indexOf('Humidity') > -1 || i == 'Light') ? '%' : '°C') ),
		            $('<td>').text(parseFloat(item[1]).toFixed(2) + ((i.indexOf('Humidity') > -1 || i == 'Light') ? '%' : '°C') )
		        ).appendTo('#measurementTable');
				} else {

			   	var $tr = $('<tr>').append(
		            $('<td>').text(i),
		            $('<td>').text(parseFloat(item).toFixed(2) + ((i.indexOf('Humidity') > -1 || i == 'Light') ? '%' : '°C') )
		        ).appendTo('#measurementTable');
				}
			});
	}

	$(document).ready(function(){
		var refresher = setInterval(function(){
			callAjax('/api_data', callDataApi);
		}, 5000)
		callAjax('/api_data', callDataApi);

		$('.controlImg').click(function(){
			var classes = ['inactive', 'active','auto'];
			var state = classes[($.inArray($(this).attr('state'), classes)+1)%classes.length];
	    $(this).attr('state', state);
		});

		$('#lampToggle').click(function(){
			if($(this).attr('state') == 'active'){
					callAjax("/turnOnLights", function(){});
			} else if($(this).attr('state') == 'inactive'){
					callAjax("/turnOffLights", function(){});
			} else if($(this).attr('state') == 'auto'){
					callAjax("/setAutoLights", function(){});
			}
		});

		$('#fanToggle').click(function(){
			if($(this).attr('state') == 'active'){
						callAjax("/turnOnFan", function(){});
			} else if($(this).attr('state') == 'inactive'){
					callAjax("/turnOffFan", function(){});
			} else if($(this).attr('state') == 'auto'){
					callAjax("/setAutoFan", function(){})
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
