import Ember from 'ember';

export default Ember.Route.extend({
  actions: {
    sendEmail: function() {
      var controller = this.get("controller");
      var message = controller.get("newEmail");
      var fromEmail = controller.get("yourEmail");
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
       });
      this.get("controller").set("newEmail", "");
      this.get("controller").set("yourEmail", "");
    },
  }
});
