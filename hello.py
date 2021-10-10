from flask import Flask, request, render_template
import non_plan_admission

app = Flask(__name__)

@app.route("/")
def hello_world():
	return render_template('main.html')

@app.route('/', methods=['POST'])
def my_form_post():
	text = request.form['text']
	print(text)

@app.route('/my-link/')
def my_link():
	non_plan_admission.main()
	return 'Click.'
