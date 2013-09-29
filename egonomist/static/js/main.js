var ids = [];

$(function() {
	$( ".select-button" ).click(function(event) {
		event.preventDefault();

		if ($(this).hasClass('selected')) {
			$(this).html("Select").removeClass("selected ").addClass("btn-info");
			var removeItem = $(this).data("id");   // item do array que deverÃ¡ ser removido
			 
			ids = jQuery.grep(ids, function(value) {
        		return value != removeItem;
        	});
        	console.log(ids);
		} else {
			$(this).html("Selected <span class='glyphicon white glyphicon-ok'></span>").addClass("selected btn-success").removeClass("btn-info");
			ids.push($(this).data("id"));
			console.log(ids);
		}
	});

	$("#sendSelected").click(function(event){
		$.ajax({
		    type: "GET",
		    url: "/selected",
		    data: ids,
		    success: function(response) {
		        
		    }
		});
	});
});