from flask import Flask

from cbr.core import main as core_main


app = Flask(__name__)

@app.route('/')
def index():
    output = core_main.run([None,"Real Madrid", "Barcelona"])
    print "output: %s" % output
    return output


if __name__ == '__main__':
    app.run(debug=True)