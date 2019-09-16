from flask import Flask, request, jsonify
from text2img import text2img, img2base64

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to Stegoman! A collection of API endpoints useful for steganography"


@app.route('/text2img', methods=['POST'])
def txt_to_img():
    res = {
        'error': 'JSON payload required'
    }
    status_code = 400 # Bad request

    if request.headers['Content-Type'] == 'application/json':
        req = request.json
        try:
            img = text2img(**req)
            img_b64 = img2base64(img)
            res['img'] = img_b64
            del res['error']
            status_code = 200 # OK
        except Exception as e:
            res['error'] = 'Bad params'

    res = jsonify(res)
    res.status_code = status_code    
    return res


if __name__ == '__main__':
    app.run(debug=True)