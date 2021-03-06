from flask import Flask, render_template, request, url_for
from src.charts import create_subplot
import os

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
	return render_template('index.html')

@app.route('/tools', methods = ['GET', 'POST'])
def tools():
	if request.method == 'POST':
		owner_name = request.form['name']
		create_subplot(data_folder = 'data', owner_name = owner_name, 
			file_name = 'standings.png', output_folder = 'static')
		# sleep(2)
		return render_template('tools.html')
	else:
		return render_template('error.html')

if __name__ == "__main__":
	app.run(debug = True)