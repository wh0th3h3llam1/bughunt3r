function cveSearch(id) {
	// var x = '#' + id + "_cpe"
	var info = $('#' + id).attr('data-info')
	var url = $('#' + id).attr('data-url')
	console.log(url);
	// console.log(url + "/" + info);
	document.location.href = url
}