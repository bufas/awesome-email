from flask import Flask, send_from_directory, render_template, request, jsonify
from emailhelper import EmailDataHandler, EmailSender
import logging

app = Flask(__name__)
app.config.from_object('config_prod')

stream_handler = logging.StreamHandler()
app.logger.addHandler(stream_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('App started')

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/send_mail', methods=['POST'])
def send_mail():
  # Providers
  providers = [
    ('emailproviders.mandrillprovider', app.config['MANDRILL_API_KEY']),
    ('emailproviders.mailgun', app.config['MAILGUN_API_KEY'])
  ]

  # Verify that all required post variables are present
  dataHandler = EmailDataHandler(
    request.form.get('email_from', ''),
    request.form.get('email_to', ''),
    request.form.get('email_subject', ''),
    request.form.get('email_message', '')
  )

  # Check the posted data for errors
  validationErrors = dataHandler.getErrors()
  if validationErrors is not None:
    return jsonify({'status': 'error', 'reason': 'validation', 'errors': validationErrors})

  # The data is valid, send emails
  emailSender = EmailSender(dataHandler, providers)
  res = emailSender.send()

  # Check for errors
  if not res['errors']:
    # All emails sent successfully
    return jsonify({'status': 'success'})
  else:
    return jsonify({'status': 'error', 'reason': 'email', 'failed': res['errors']})

@app.route('/<path:filename>')
def resources(filename):
  return send_from_directory('static', filename)

if __name__ == '__main__':
  app.run()
