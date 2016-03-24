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
            "from_email": "info@devhouseatx.com",
            "to": [
                {
                  "email": "devhouseatx@gmail.com",
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
         alert("Email Delivery Status! " + response[0].status);
         console.log(response); // if you're into that sorta thing
         if(response[0].status === "sent") {
           $('.email').val('');
           $('.email-message').val('');
         }
       });
  } else {
    alert("Invalid Email Address");
  }
});
