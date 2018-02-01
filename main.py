import flask
import sys
import tempfile
import os

from models import *

app = flask.Flask(__name__)
app.secret_key = 'fj3bklLKknb786hJHf'


@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'POST':
        if 'file' not in flask.request.files:
            flask.flash('No file part')
            return flask.redirect(flask.request.url)

        file = flask.request.files['file']
        if file.filename == '':
            flask.flash('No selected file')
            return flask.redirect(flask.request.url)

        if file and not allowed_file(file.filename):
            flask.flash('Not allowed file type')
            return flask.redirect(flask.request.url)

        upl = tempfile.NamedTemporaryFile(delete=False)
        upl.write(file.read())
        result = recognize(upl.name)
        app.logger.info(result)
        return flask.render_template('results.html', data=result, image=flask.url_for('images', image=os.path.basename(upl.name)))
    else:
        return flask.render_template('index.html')


@app.route('/images/<image>', methods=['GET'])
def images(image):
    file_dir = tempfile.gettempdir()
    try:
        return flask.send_from_directory(file_dir, image)
    finally:
        os.remove(os.path.join(file_dir, image))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in set(['png', 'jpg', 'jpeg'])


def recognize(filename):
    return resnet50.run(filename)


if __name__ == '__main__':
    debug = True
    if os.getenv('FLASK_ENVIROMENT', 'development') == 'production':
        debug = False
    sys.exit(app.run(host='0.0.0.0', debug=debug))
