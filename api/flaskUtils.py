from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/api/temps", methods=['GET'])
def getTemps():
    return