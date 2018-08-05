from flask import Flask, Response

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World'

@app.route('/container1', methods=['GET'])
def hello_world_path():
    return 'Flask Dockerized'


@app.route('/v1/container1', methods=['GET'])
def hello_world_path2():
    return 'Flask Dockerized 2.0'

@app.route('/v1/container2', methods=['GET'])
def hello_world_path2():
    return 'Flask Dockerized 3.0'


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=443)
