// function exportFile(id, domain) {
function exportFile() {
	// console.log(id)
	// console.log(domain);
	$('body').toast({
		title: 'Preparing Download',
		// message: 'Preparing Download',
		showProgress: 'bottom',
		classProgress: 'teal',
		displayTime: 3500,
	});
	var url = $('#export').attr('data-url')
	console.log(url);
	document.location.href = url
}