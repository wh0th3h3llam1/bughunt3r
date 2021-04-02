COLORS = ['red', 'orange', 'yellow', 'olive', 'green', 'teal', 'blue', 'violet', 'purple', 'pink', 'brown', 'grey']

function toggleTheme() {
	// if ($('#theme').is(":checked")) {
	// 	$(".ui").removeClass("inverted");	
	// }
	
	if (localStorage.getItem("theme") == "dark") {
		$('#theme').prop('checked', false);
		localStorage.setItem("theme", "light")
		$(".ui").removeClass("inverted");
		$("body").css("background-color", "#FFF");
		$("body").css("color", "#000");
		$(".segment").removeClass("black");	
		// $("table").removeClass("grey");
		
	}
	else {
		$('#theme').prop('checked', true);
		localStorage.setItem("theme", "dark")
		$(".ui").addClass("inverted");	
		$("body").css("background-color", "#2E2E2E");
		$("body").css("color", "#FFF");
		$(".segment").addClass("black");	
		COLORS.forEach(element => {
			$("table").removeClass(element);
		});
		$("table").addClass("black");	
	}
}

function setTheme() {
	if (localStorage.getItem("theme") == "dark") {
		$('#theme').prop('checked', true);
		localStorage.setItem("theme", "dark")
		$(".ui").addClass("inverted");	
		$("body").css("background-color", "#2E2E2E");
		$("body").css("color", "#FFF");
		$(".segment").addClass("black");	
		COLORS.forEach(element => {
			$("table").removeClass(element);
		});
		$("table").addClass("black");	
	}
	else {
		$('#theme').prop('checked', false);
		localStorage.setItem("theme", "light")
		$(".ui").removeClass("inverted");
		$("body").css("background-color", "#FFF");
		$("body").css("color", "#000");
		$(".segment").removeClass("black");	
		// $("table").removeClass("grey");
		
	}
}