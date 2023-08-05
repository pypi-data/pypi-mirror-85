# flask_tinify ![Build](https://github.com/Minecraftschurli/flask_tinify/workflows/Build/badge.svg)
An adaption of [tinify](https://github.com/tinify/tinify-python) as a flask extension

## Installation
Install the API client:

```shell
pip install flask-tinify
```

## Usage
```python
from flask import Flask
from flask_tinify import Tinify

app = Flask(__name__)
tinify = Tinify(app)
```

## Basic example
```python
from flask import Flask, request
from flask_tinify import Tinify

app = Flask(__name__)
tinify = Tinify(app)

@app.route('/tinify', methods=['POST'])
def hello_png():
    image = request.form['image']
    if not image:
        return '', 400
    with image.strem as stream:
        tinify.from_buffer(stream.read()).to_buffer()
```
