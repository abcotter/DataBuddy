import pytesseract as tess
import sys
import re
import csv
from PIL import Image
import os
from pathlib import Path
from flask import Flask, request, jsonify, make_response, send_file
from flask_cors import CORS
import base64
import io, os, glob

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


@app.route("/")
def hello_world():
    return "loser!"


@app.route("/getCSV", methods=["POST"])
def get_csv():
    data = request.form
    # imgdata = base64.b64decode(img)
    image = Image.open(io.BytesIO(base64.b64decode(data["file"])))
    text = tess.image_to_string(image)
    result = re.split("\n", text)
    resultList = [float(i.replace(",", "")) for i in result[::-1] if isfloat(i)]
    return {"result": resultList}

