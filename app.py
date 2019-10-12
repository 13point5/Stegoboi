from flask import Flask, request, jsonify
from utils import *


app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome to Stegoman! A collection of API endpoints useful for steganography"


@app.route('/text2img', methods=['POST'])
def img_from_text():
    res = { 'error': 'JSON payload required' }
    status_code = 400 # Bad request

    if request.headers['Content-Type'] == 'application/json':
        req = request.json

        try:
            img = text_to_img(text = req["text"])
            img_b64 = img_to_b64(img=img, format=req.get("format", "PNG"))
            res['img'] = img_b64
            del res['error']
            status_code = 200

        except Exception as e:
            res['error'] = 'Bad params'

    res = jsonify(res)
    res.status_code = status_code    
    return res


if __name__ == '__main__':
    app.run(debug=True)