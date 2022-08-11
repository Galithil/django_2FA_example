
function get_qr_code(){
	
	$.ajax({
	url : "/auth/api/getqrcode",
	method : "GET"

	}).done(function(data){
		console.log(data);
		$("#qrcodeimg").attr("src", 'data:image/png;base64,'+data);

	}).fail(function(){
		$("#modal_internal_text").html('Login Failed');
		console.log("Failed");

	});

}

function activate_tfa(){
	$.ajax({
	url : "/auth/api/settfa",
	method : "GET"

	}).done(function(data){
		get_qr_code();
		$("#modal_internal_text").html('Two factor authentication activated');
		$("#dialog_modal").modal('show');

	}).fail(function(){
		$("#modal_internal_text").html('Two factor authentication failed');
		$("#dialog_modal").modal('show');
		console.log("Failed");

	});

}
function logout(){
	$.ajax({
	url : "/auth/api/logout",
	method : "GET"

	}).done(function(data){
		window.location = data;

	}).fail(function(){
		console.log("Failed");
	});

}

$(document).ready(function(){
	get_qr_code();
	$("#activate_btn").click(activate_tfa);
	$("#logout_btn").click(logout);
		

});
