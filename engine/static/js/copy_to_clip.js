function copyToClip(id) {
	console.log(id);
	// var copyText = document.getElementById(id);
	var copyText = document.getElementById(id).textContent;
	// console.log(copyText.textContent);
	copyText.select();
	copyText.setSelectionRange(0, 99999);
	document.execCommand("copy");
}