function send_credentials(){
	var data = {email:$("#floatingInput").val(), password : $("#floatingPassword").val(),totp:$("#TFAInput").val()};
	$.ajax({
	url : "/auth/api/fetchuser",
	data : JSON.stringify(data),
	method : "POST"


	}).done(function(data){
		console.log("Success");
		window.location = data;

	}).fail(function(xhr, textStatus, errorThrown){
		if(xhr.status == 401){
			$("#dialog_modal").modal('show');

		}else{
			$("#TFAInput").val('');
			$("#dialog_modal").modal('show');
			console.log(xhr.status);
			console.log(textStatus);
			console.log(errorThrown);
			console.log("Failed");
		}
	});
}

$("#main_form").submit(function(e){
e.preventDefault();
});

$("#signinbutton").click(function(){
	send_credentials();
});
$("#tfa_btn").click(function(){
	send_credentials();
});
