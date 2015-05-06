from flask import Flask, send_from_directory, render_template, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from emailhelper import EmailDataHandler, EmailSender
import logging
import os

app = Flask(__name__)

# Load the correct configuration
if os.environ.get('TESTING', False):
  app.config.from_object('config_test')
else:
  app.config.from_object('config_prod')

db = SQLAlchemy(app)

from model import ProviderModel

stream_handler = logging.StreamHandler()
app.logger.addHandler(stream_handler)
app.logger.setLevel(logging.INFO)


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/send_mail', methods=['POST'])
def send_mail():
  # Providers
  providers = [(p.name, p.key) for p in ProviderModel.query.order_by('rank').all()]

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
  emailSender = EmailSender(dataHandler, providers, logger=app.logger)
  res = emailSender.send()

  # Check for errors
  if not res['errors']:
    # All emails sent successfully
    return jsonify({'status': 'success'})
  else:
    return jsonify({'status': 'error', 'reason': 'email', 'failed': res['errors']})


if __name__ == '__main__':
  app.run()
