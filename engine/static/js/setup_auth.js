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