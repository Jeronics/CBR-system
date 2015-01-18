from flask import Flask
from flask import render_template

from cbr.core import main as core_main


app = Flask(__name__)

@app.route('/')
def index():
    output = core_main.run([None, "Real Madrid", "Barcelona"])
    return render_template('index.html', team1=, prediction=output)


if __name__ == '__main__':
    app.run(debug=True)