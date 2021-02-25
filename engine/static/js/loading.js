function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}

function onSubmit(event) {
	event.preventDefault();
	console.log("In Submit");
	var url = $('#url').val();
	// var expression =  /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi;
	var expression = "/^(?:(ftp|http|https)?:\/\/)?(?:[\w-]+\.)+([a-z]|[A-Z]|[0-9]){2,6}$/gi";
	console.log("URL Provided: " + url);
	console.log("Checking conditions");
	if(url === "")
	{
		console.log("Empty");
		$('body').toast({
			class: 'error',
			message: `Please enter a url`
		});
	}
	else if(url.match(expression))
	{
		console.log("Url match");
		$('body').toast({
			class: 'success',
			message: `Its a URL`
		});
	}
	else
	{
		console.log("In else");
		$('#btn').addClass('loading');
		$('.form').addClass('blue');
		$('.form').addClass('double');
		$('.form').addClass('loading');
		$('body')
		.toast({
			title: 'Subdomain Scan Started',
			message: 'It may take a while to run the scan!'
		});

		// sleep(3000).then(() => {
		setTimeout(() => {console.log("slept for 3 sec");}, 3000);
		// })
	}
}