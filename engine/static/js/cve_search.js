function cveSearch(id) {
	// var x = '#' + id + "_cpe"
	var info = $('#' + id).attr('data-info');

	// cpe:/<part>:<vendor>:<product>:<version>:<update>:<edition>:<language>
	
	var cve_info = info.split(":");
	
	var part = cve_info[1];
	var vendor = cve_info[2];
	var product = cve_info[3];
	var version = cve_info[4];
	var update = cve_info[5];
	var edition = cve_info[6];
	var language = cve_info[7];
	
	var url = $('#' + id).attr('data-url');
	console.log(url);
	// console.log(url + "/" + info);
	// document.location.href = url
}