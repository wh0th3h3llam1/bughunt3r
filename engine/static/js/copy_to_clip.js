// function trim(str) {
// 	return str.replace(/^\s+|\s+$/g,"");
// }

function copyToClip(id) {
	var dom = $("#" + id + "_a").html();
	console.log(dom);
	if (copy(dom)) {
		$('body')
		.toast({
			message: 'Copied to Clipboard',
			class: 'success',
			showIcon: "check",
			displayTime: 3000,
		});
	}
	else {
		console.log("Error Copying to Clipboard");
		$('body')
		.toast({
			message: 'Error Copying to Clipboard',
			class: 'error',
			showIcon: "times",
			displayTime: 3000,
		});
	}
}

function copy(text) {
	var input = document.createElement('input');
	input.setAttribute('value', text.trim());
	document.body.appendChild(input);
	input.select();

	var result = document.execCommand('copy');
	document.body.removeChild(input);
	
	return result;
}