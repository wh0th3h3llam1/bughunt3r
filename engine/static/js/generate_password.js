function generatePassword() {
	var string = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz._-/%@#?'; 
	var len = string.length; 
	let pwd = "";
	var min = 14;
	var max = 21;
	var pwd_len = Math.floor(Math.random() * (max - min + 1)) + min;

	// console.log(window.crypto.getRandomValues([15, 20]));
	for (let i = 0; i < pwd_len; i++ ) { 
		pwd += string[Math.floor(Math.random() * len)]; 
	}
	// $('#passwd').val = pwd;	
	document.getElementById("passwd").value = pwd;	
	event.preventDefault();
}