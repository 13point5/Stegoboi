from flask import Flask, request, jsonify
from text2img import text2img, img2base64

app = Flask(__name__)

@app.route('/')
def index():
    return "text to img API"


@app.route('/txtoimg', methods=['POST'])
def tx_to_img():
    if request.headers['Content-Type'] == 'application/json':
        req = request.json
        img = text2img(req["text"], font_path='Product Sans Regular.ttf')
        img_str = img2base64(img)
        res = jsonify({
            'img': img_str
        })
        res.status_code = 200 # OK
    else:
        res = jsonify({
            'error': 'JSON payload required'
        })
        res.status_code = 400 # Bad Request
    
    return res

if __name__ == '__main__':
    app.run(debug=True)