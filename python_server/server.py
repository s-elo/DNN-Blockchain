from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/<scriptName>')
def getModel(scriptName):
    return jsonify(scriptName=scriptName, age=16)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
