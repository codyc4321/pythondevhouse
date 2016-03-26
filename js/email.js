$('.new-email-button').click(function() {

    var fromEmail = $('.email').val();
    console.log('email');
    console.log(fromEmail);
    var message = $('.email-message').val();
    console.log(message);
    var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if (re.test(fromEmail)) {
        $.ajax({
            type: "POST",
            url: "https://api.postmarkapp.com/email",
            // headers: {
            //     "Access-Control-Allow-Origin": "*",
            // }
            data: {
              "From": "info@pythondevhouse.com",
              "To": "cchilder@mail.usf.edu",
              "Cc": "copied@example.com",
              "Bcc": "blank-copied@example.com",
              "Subject": "Test",
              "Tag": "Invitation",
              "TextBody": message,
              "ReplyTo": fromEmail,
              "Headers": [
                { 
                    "Name": "X-Postmark-Server-Token",
                    "Value": "ba7663a2-19ba-4a42-bf69-5b4485fcab6f"
                }
              ],
              "TrackOpens": true
            },
            contentType: "application/json",
            accepts: {
                text: "application/json"
            }
            
           }).done(function(response) {
             alert(response);
             if (response[0].status == 'rejected'){
               alert("I'm sorry, the email form isn't working.\n\nPlease email info@pythondevhouse.com\nor call 813-545-2150");
             }
             else{
               alert("Sent successfully! Thank you, I will contact you soon");
               console.log(response); // I am.
             }
             if(response[0].status === "sent") {
               $('.email').val('');
               $('.email-message').val('');
             }
           });
      } else {
        alert("Invalid Email Address");
      }
});
