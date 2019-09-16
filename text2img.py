# generate an image with given text

from PIL import Image, ImageFont, ImageDraw
import base64
from io import BytesIO


NEWLINE_CHAR = '\uFFFD'
WHITESPACE = ' '
NEWLINE_STRING = WHITESPACE + NEWLINE_CHAR + WHITESPACE


def get_line_width(font, text):
    return font.getsize(text)[0]


def get_line_height(font, text):
    return font.getsize(text)[1]


def text2img(text, font_path='Product Sans Regular.ttf', font_size=16, img_mode="L", color='#000000', bg_color='#FFFFFF', lr_padding=8, max_width=300):

    font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
    text = text.replace('\n', NEWLINE_STRING)

    effective_width = max_width - 2*lr_padding # centered text
    line_height = get_line_height(font, text)

    lines = []
    line = ''
    max_line_width = 0

    for word in text.split():
        if word == NEWLINE_CHAR: # user specified new line
            lines.append(line.strip())
            lines.append('')
            line = ''
        elif font.getsize(line + WHITESPACE + word)[0] <= effective_width: # word can fit in same line
            line += word + WHITESPACE
        else: # word can't fit in same line
            lines.append(line.strip())
            line = word + WHITESPACE
    
    if line: lines.append(line.strip())
    
    max_line_width = get_line_width(font, max(lines, key=len))
    
    img_height = line_height * len(lines)
    img_width = max_line_width + 2*lr_padding

    img = Image.new(img_mode, (img_width, img_height), bg_color) # use "L" for black and white
    canvas = ImageDraw.Draw(img)

    for idx, line in enumerate(lines):
        canvas.text((lr_padding, idx * line_height), line, color, font=font)
    
    return img


def img2base64(img, format="PNG"):
    buffered = BytesIO()
    img.save(buffered, format=format) # "PNG", "JPEG"
    return str(base64.b64encode(buffered.getvalue()))


if __name__ == '__main__':
    text = 'asghbgebvfe vhrnhvf wvsnhufvs\n svdkhfdf'
    font_path = 'Product Sans Regular.ttf'
    ps = {
        'text': text,
        'font_path': font_path,
        'color': '#888888',
        'bla': 2
    }
    try:
        image = text2img(**ps)
        image.save('tst.png')
    except Exception as e:
        print(e)
        print(type(e))
        print(str(e))
    # image = text2img(text=text, font_path=font_path)
    
    # img_str = img2base64(image)
    # print(img_str)