from flask import Flask, send_from_directory, render_template, request, jsonify
import json
import sys

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/send_mail', methods=['POST'])
def send_mail():

  info = dict({
    'from'    : request.form['EMAIL_FROM'],
    'to'      : request.form['EMAIL_TO'].split(','),
    'subject' : request.form['EMAIL_SUBJECT'],
    'message' : request.form['EMAIL_MESSAGE']
  })

  # try:
  #   import mailgunsender
  #   response = mailgunsender.send(info, apiKey=app.config['MAILGUN_API_KEY'])
  #   return response
  # except:
  #   return json.dumps({'lol' : str(sys.exc_info()[0])})
  #   pass

  # try:
  #   import mandrillsender
  #   response = mandrillsender.send(info, apiKey=app.config['MAILGUN_API_KEY'])
  #   return jsonify(response)
  # except:
  #   # TODO Try next service
  #   pass


@app.route('/<path:filename>')
def resources(filename):
  return send_from_directory('static', filename)

if __name__ == '__main__':
  app.config.from_object('config_prod')
  app.run()
