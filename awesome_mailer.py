from flask import Flask, send_from_directory
import mandrill
app = Flask(__name__)

@app.route('/')
def index():
  return send_from_directory('static', 'index.html')

@app.route('/send_mail', methods=['POST'])
def send_mail():
  # TODO send email
  try:
    mandrill_client = mandrill.Mandrill('hx5qZ-I25AcaGr16tpCU2Q')
    return mandrill_client.users.ping()
  except Mandrill.Error, e:
    print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
    raise

@app.route('/<path:filename>')
def resources(filename):
  return send_from_directory('static', filename)

if __name__ == '__main__':
  app.run(debug=True)
