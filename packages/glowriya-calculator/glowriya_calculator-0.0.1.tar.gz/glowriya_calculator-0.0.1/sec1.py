from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    x = 1 + 1
    y = sum(3, 5)
    return "hello flask"


def sum(a, b):
    return a + b