var display_time = 10000

function validateURL() {

	var url = $('#url').val();
	var url_regex =  /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi; 
	var ip_regex = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;

	if(url_regex.test(url) || ip_regex.test(url))
	{
		$('#url_field').removeClass('error');
		return true
	}
	else {
		$('#url_field').addClass('error');
		$('body')
		.toast({
			class: 'error',
			message: `Please Enter a valid URL or I.P. Address`
		});
		return false
	}
}


function validatePort(p) {
	p.every(function (segment) {
		console.log(p);
		return validateNum(segment, 1, 65536);
	});
}

function validateNum(input, min, max) {
    var num = +input;
    return num >= min && num <= max && input === num.toString();
}


function validatePortRange() {
	var port_range = $('#ports').val();
	if(port_range === "" || port_range == 0) {
		console.log("Empty Port Range");
		$('body').toast({
			class: 'error',
			message: `Please Enter Port Number or Port Range`
		});
		$('#port_field').addClass('error');
		return false
	}

	else {
		console.log("In else");
		if (port_range.includes("-")) {
			var p = port_range.split("-")
			p1 = p[0];
			p2 = p[1];
			if (validateNum(p1, 1, 65535) && validateNum(p2, 1, 65535)) {
				if (!(p1 < p2)) {
					$('body').toast({
						class: 'error',
						title: `Port Range Invalid`,
						message: `It should be in a format x-y and x must be less than y`
					});
					return false
					
				}
				$('#port_field').removeClass('error');
				return true
			}

			else {
				$('body').toast({
					class: 'error',
					title: `Port Range Invalid`,
					message: `Port Range must be between 1 and 65535`
				});
				$('#port_field').addClass('error');
				return false
			}
		}

		// Port Number
		else {
			console.log("In Else else");
			var x = validateNum(port_range, 1, 65535);
			if (!x) {
				$('body').toast({
					class: 'error',
					title: `Port Number Invalid`,
					message: `Port Number must be between 1 and 65535`
				});
				$('#port_field').addClass('error');
				return false
			}
			else {
				// $('body').toast({
				// 	class: 'success',
				// 	message: `Port Range Valid`
				// });
				$('#port_field').removeClass('error');
				return true
			}
		}
	}
}


function subdomainScanStarted(event) {
	var url = $('#url').val();
	if(url === "")
	{
		console.log("Empty");
		$('body').toast({
			class: 'error',
			message: `Please enter a URL or I.P. Address`
		});
		event.preventDefault();
	}
	else if(validateURL())
	{
		console.log("True");
		$('.ui.primary.button').addClass('double loading');
		$('body').toast({
			title: 'Subdomain Scan Started',
			message: 'It may take a while to run the scan!',
			showProgress: 'bottom',
			classProgress: 'red',
			displayTime: display_time
		});
		// var link = $('#btn').attr('data-url')
		// console.log(link);
		// document.location.href = link;
	}
	else
	{
		console.log("False");
		event.preventDefault();
	}
}


function portScanStarted(event) {
	// event.preventDefault();
	var url = $('#url').val();
	// console.log(url);
	if(url === "")
	{
		console.log("Empty URL");
		$('body').toast({
			class: 'error',
			message: `Please enter a URL or I.P. Address`
		});
		event.preventDefault();
	}
	else if(validateURL() & validatePortRange())
	{
		console.log("True");
		$('.ui.primary.button').addClass('double loading');
		$('body').toast({
			title: 'Port Scan Started',
			message: 'It may take a while to run the scan!',
			showProgress: 'bottom',
			classProgress: 'blue',
			displayTime: display_time
		});
		var link = $('#btn').attr('data-url')
		console.log(link);
		document.location.href = link;
	}
	else
	{
		$('.ui.primary.button').removeClass('double loading');
		console.log("False");
		event.preventDefault();
	}
	// $('body').toast({
	// 	title: 'Port Scan Started',
	// 	message: 'It may take a while to run the scan!',
	// 	showProgress: 'bottom',
	// 	classProgress: 'blue',
	// 	displayTime: display_time
	// });
	// $('.ui.primary.button').addClass('double loading');
}


function activeSubdomainScanStarted() {
	$('body').toast({
		title: 'Active Subdomain Scan Started',
		message: 'It may take a while to run the scan!',
		showProgress: 'bottom',
		classProgress: 'green',
		displayTime: display_time,
	});
	$('#active_subdomain_btn').addClass('green double loading');
	var url = $('#active_subdomain_btn').attr('data-url')
	console.log(url);
	document.location.href = url
}


function eyewitnessScanStarted() {
	
	$('body').toast({
		title: 'Eye Witness Scan Started',
		message: 'It may take a while to run the scan!',
		showProgress: 'bottom',
		classProgress: 'orange',
		displayTime: display_time,
	});
	$('#eyewitness_btn').addClass('orange double loading');
	var url = $('#eyewitness_btn').attr('data-url')
	console.log(url);
	document.location.href = url;
}


function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}