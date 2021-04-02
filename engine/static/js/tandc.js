function termsAndConditions() {
	if (localStorage.getItem("terms_conditions") != "yeah") {
		$('.ui.modal')
		.modal({
			closable: false,
			onApprove : function() {
				localStorage.setItem("terms_conditions", "yeah")
				setupAuth();
			}
		}).modal('show');
	}
	else {
		setupAuth();
	}
}

function setupAuth() {
	// if (localStorage.getItem("gui_choice") != "nah") {
	if (sessionStorage.getItem("gui_choice") != "nah") {
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
						// localStorage.setItem("gui_choice", "nah")
						sessionStorage.setItem("gui_choice", "nah")
					}
				}
			]
		});
	}
}