function validateURL() {
	
	var url = $('#url').val();
	var expression =  /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi; 
	var regex = new RegExp(expression); 
	console.log(url);
	// if(url.match(expression))
	// {
	// 	return true
	// }
	// else {
	// 	return false
	// 	$('body')
	// 	.toast({
	// 		class: 'error',
	// 		message: `Please Enter a valid URL`
	// 	});
	// }
}

function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}