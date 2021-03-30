// Change the type of input to password or text
function togglePassword()
{
	var chkbox = document.getElementById("passwd");
	// var chkbox_val = document.getElementById("passwd").val();
	// console.log(chkbox_val);

	// if (chkbox.type === "password")
	if ($('#show_password').is(':checked'))
	{
		chkbox.type = "text";
	}
	else
	{
		chkbox.type = "password";
	}
}
