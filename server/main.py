from flask import Flask, send_from_directory
app = Flask(__name__)

@app.route('/')
def index():
  return send_from_directory('../client', 'index.html')

@app.route('/send_mail', methods=['POST'])
def send_mail():
  # TODO send email
  pass

@app.route('/<path:filename>')
def resources(filename):
  return send_from_directory('../client', filename)

if __name__ == '__main__':
  app.run(debug=True)