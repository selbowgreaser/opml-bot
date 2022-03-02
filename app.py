from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    with open('vk_bot/graph.html') as f:
        return f.read()


if __name__ == '__main__':
    app.run()
