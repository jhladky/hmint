from flask import Flask, render_template
from core import DEBUG, TESTING

app = Flask(__name__)

app.config.update(
    DEBUG=DEBUG,
    TESTING=TESTING
)


@app.route('/')
def slash():
    return render_template('index.html')
