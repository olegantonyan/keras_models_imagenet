import quart
import sys
import tempfile
import os

import models.resnet50

app = quart.Quart(__name__)


@app.route('/', methods=['GET', 'POST'])
async def index():
    if quart.request.method == 'POST':
        files = await quart.request.files
        f = files['file']
        upl = tempfile.NamedTemporaryFile(delete=False)
        upl.write(f.read())
        return await quart.render_template('results.html', data=recognize(upl.name), image=quart.url_for('images', image=os.path.basename(upl.name)))
    else:
        return await quart.render_template('index.html')


@app.route('/images/<image>', methods=['GET'])
async def images(image):
    file_dir = tempfile.gettempdir()
    try:
        return await quart.send_from_directory(file_dir, image)
    finally:
        os.remove(os.path.join(file_dir, image))


def recognize(filename):
    return models.resnet50.run(filename)


if __name__ == '__main__':
    sys.exit(app.run(host='0.0.0.0', debug=True))
