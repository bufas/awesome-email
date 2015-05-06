
$.formUtils.addValidator({
  name : 'list_of_emails',
  validatorFunction : function(value) {
    var addresses = value.split(',');
    return addresses.every(function (email) {
      return $.formUtils.validators.validate_email.validatorFunction(email);
    });
  },
  errorMessage : 'Must be a comma separated list of email addresses',
  errorMessageKey: 'badEmailList'
});

$(function () {

  $.validate({
    modules : 'html5',
    onSuccess : function() {
      $('#submit_button').val('Sending emails');
      $.post('/send_mail', $('#emailForm').serialize(), function (data) {
        $('#submit_button').val('Submit');

        var status = $('#status');
        var extra_info = $('#extra_error_info');
        status.empty();
        extra_info.empty();

        if (data.status == 'success') {
          // All emails were sent successfully
          status.text('All emails successfully sent.');
          $('#emailForm').get(0).reset();
        } 
        else if (data.status == 'error' && data.reason == 'validation') {
          // A validation error occoured
          console.log(data.errors);
          status.text('A server validation error occurred')
        }
        else if (data.status == 'error' && data.reason == 'email') {
          // One or more emails were not sent
          if (data.failed.length > 1) {
            status.text('Sending to the following receivers failed:');
            data.failed.forEach(function (e) {
              extra_info.append(e + '<br>');
            });
          } else {
            status.text('Sending to '+data.failed[0]+' failed.');
          }
        }
      });

      return false;
    }
  });

});