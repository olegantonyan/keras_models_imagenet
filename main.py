import flask
import sys
import tempfile
import models.resnet50

app = flask.Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'POST':
        f = flask.request.files['file']
        with tempfile.NamedTemporaryFile() as upl:
            upl.write(f.read())
            return flask.render_template('results.html', data=recognize(upl.name))
    else:
        return flask.render_template('index.html')


def recognize(filename):
    return models.resnet50.run(filename)


if __name__ == '__main__':
    sys.exit(app.run(debug=True))
