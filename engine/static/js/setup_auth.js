function setupAuth() {
	if (localStorage.getItem("gui_choice") != "nah") {
		$('body')
		.toast({
			title: 'Set Up GUI Authentication',
			message: 'It is recommended to setup authentication. Would you like to setup now?',
			displayTime: 0,
			showIcon: 'user shield',
			// class: 'black',
			actions: [
				{
					text: 'Yup',
					icon: 'check',
					class: 'green',
					click: function() {
						$('body').toast({message:'You clicked "yes", toast closes by default'});
						var link = $('#set_auth').attr('data-url')
						console.log(link);
						document.location.href = link;
					}
				},
				{
					text: 'Nah',
					icon: 'close',
					class: 'icon red',
					click: function() {
						localStorage.setItem("gui_choice", "nah")
					}
				}
			]
		});
	}
}

function setupAuthentication(event) {
	
	$('.ui.green.button').addClass('double loading');

	var user_name = $('#user_name').val();
	var passwd = $('#passwd').val();
	
	if (validateUserName(user_name) && validatePassword(passwd)) {
		// var link = $('#setup').attr('data-url')
		// console.log(link);
		// document.location.href = link;
	}
	else {
		event.preventDefault();
	}
}

function validateUserName(user_name) {
	if(user_name === "")
	{
		console.log("Empty");
		$('body').toast({
			class: 'error',
			message: `Please enter User Name`
		});
		$('.ui.green.button').removeClass('double loading');
		return false
	}
	return true
}

function validatePassword(passwd) {
	if(passwd === "")
	{
		console.log("Empty");
		$('body').toast({
			class: 'error',
			message: `Please enter Password`
		});
		$('.ui.green.button').removeClass('double loading');
		return false
	}
	return true
}