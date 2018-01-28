import flask
import sys
import tempfile
import os

import models.resnet50

app = flask.Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'POST':
        f = flask.request.files['file']
        upl = tempfile.NamedTemporaryFile(delete=False)
        upl.write(f.read())
        return flask.render_template('results.html', data=recognize(upl.name), image=flask.url_for('images', image=os.path.basename(upl.name)))
    else:
        return flask.render_template('index.html')


@app.route('/images/<image>', methods=['GET'])
def images(image):
    file_dir = tempfile.gettempdir()
    try:
        return flask.send_from_directory(file_dir, image)
    finally:
        os.remove(os.path.join(file_dir, image))


def recognize(filename):
    return models.resnet50.run(filename)


if __name__ == '__main__':
    sys.exit(app.run(debug=True))
