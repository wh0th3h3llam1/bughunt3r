function exportFile() {
	var c = "";
	if (localStorage.getItem("theme") == "dark") {
		c = "black";
	}
	// else {
	// 	c = "";
	// }
	$('body').toast({
		title: 'Preparing Download',
		showProgress: 'bottom',
		showIcon: "download",
		class: c,
		classProgress: "teal",
		displayTime: 3500,
	});
	var url = $('#export').attr('data-url')
	console.log(url);
	document.location.href = url
}