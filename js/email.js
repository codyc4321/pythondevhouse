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
        url: "https://mandrillapp.com/api/1.0/messages/send.json",
        data: {
          "key": "Dpnhfrv6lMKKVpcICDVGqw",
          "message": {
            "from_email": "info@pythondevhouse.com",
            "to": [
                {
                  "email": "cchilder@mail.usf.edu",
                  "name": "",
                  "type": "to"
                },
                // {
                //   "email": "RECIPIENT_NO_2@EMAIL.HERE",
                //   "name": "ANOTHER RECIPIENT NAME (OPTIONAL)",
                //   "type": "to"
                // }
              ],
            "headers": {
              "Reply-To": fromEmail
            },
            "autotext": "null",
            "subject": "Website Inquiry",
            "text": message
          }
        }
       }).done(function(response) {
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
