function validateURL() {
	
	// var url = $('#url').val();
	// var expression =  /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi; 
	// var regex = new RegExp(expression); 
	// // if( $('.ui.form').form('is valid', 'email')) {
	// 	// email is valid
	// if(url.match(expression))
	// {
	// 	return true
	// }
	// else {
	// 	return false
	// }

	$('.ui.form')
	.form({
		fields: {
			url: {
				identifier  : 'url',
				rules: [
					{
						type   : 'url',
						prompt : 'Please Enter a valid URL'
					}
				]
			  },
		},
		inline: true,
		// on: 'blur'
	});
}

function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
 }

function checkURL() {
	$('.form').addClass('loading');
	sleep(3000).then(() => {
		console.log("slept for 3 sec");
	})

	// var url = $('#url').val();
	// var expression =  /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi; 
	// var regex = new RegExp(expression); 
	$('.ui.form')
	.form({
		fields: {
			url: {
				identifier  : 'url',
				rules: [
					{
						type   : 'url',
						prompt : 'Please Enter a valid URL'
					}
				]
			  },
		},
		inline: true,
		// on: 'blur'
	});
	if($('.ui.form').form('is valid', 'url')) {
		$('.form').removeClass('loading');
		// document.get
	}
	else {
		// url is invalid
		$('body')
		.toast({
			class: 'error',
			message: `Please Enter a valid URL`
		});
	}
	// if(url.match(expression))
	// {
	// 	return true
	// }
	// else {
	// 	return false
	// }
}