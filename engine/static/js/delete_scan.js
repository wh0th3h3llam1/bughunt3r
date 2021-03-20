function deleteScan(id) {
	console.log(id);
	// window.location = ""
	var url = $('#delete').attr('data-url')
	console.log(url);
	document.location.href = url
}