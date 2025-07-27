export function getStravaToken(client_code) {
	$.ajax({
		type: "GET",
		url: "http://127.0.0.1:5000/get_token",
		data: { client_code: client_code },
		success: callbackFunc,
	});
}

function callbackFunc(response) {
	console.log("Data processed : " + response.reply);
}
