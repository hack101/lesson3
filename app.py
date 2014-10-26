from flask import Flask, redirect, request, url_for, render_template
from firebase import firebase

# config
# server will reload on source changes, and provide a debugger for errors
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__) # consume the configuration above

firebase = \
    firebase.FirebaseApplication('https://fiery-torch-8827.firebaseio.com', None)

@app.route('/')
def index():
  return render_template('index.html')

# decorator which tells flask what url triggers this fn
@app.route('/messages')
def messages():
  result = firebase.get('/messages', None)
  return render_template('list.html', messages=result)

@app.route('/submit_message', methods=['POST'])
def submit_message():
  message = {
    'body': request.form['message'],
    'who': request.form['who']
  }
  firebase.post('/messages', message)
  return redirect(url_for('messages'))

if __name__ == "__main__":
  app.run()