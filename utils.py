import base64
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw

TOT_LEN_MAX = 1 << 10
WORD_LEN_MAX = 1 << 6

NEWLINE_CHAR = '\uFFFD'
WHITESPACE = ' '
NEWLINE_STRING = WHITESPACE + NEWLINE_CHAR + WHITESPACE


def get_line_width(font, text):
    return font.getsize(text)[0]


def get_line_height(font, text):
    return font.getsize(text)[1]


def text_to_img(text, font_path='Product Sans Regular.ttf', font_size=16, img_mode="L", color='#000000', bg_color='#FFFFFF', lr_padding=16, max_width=300):

    font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
    text = text
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
    
    if line:
        lines.append(line.strip())
    
    max_line_width = get_line_width(font, max(lines, key=len))
    
    img_height = (line_height * len(lines)) + (line_height // 2) # the second term is for extra space at the bottom
    img_width = max_line_width + (2 * lr_padding)

    img = Image.new(img_mode, (img_width, img_height), bg_color) # use "L" for black and white
    canvas = ImageDraw.Draw(img)

    for idx, line in enumerate(lines):
        canvas.text((lr_padding, idx * line_height), line, color, font=font)
    
    return img


def zero_pad(max_len, data_bin):
    return '0' * (max_len - len(data_bin))


def get_char_bin(char):
    char = char.lower()
    pos = ord(char) - ord('a')
    char_bin = bin(pos)[2:]
    char_bin = zero_pad(5, char_bin) + char_bin
    return char_bin


def get_num_bin(num):
    num = int(num)
    
    if num > TOT_LEN_MAX:
        raise ValueError("Number bigger than {}".format(TOT_LEN_MAX))

    if num > WORD_LEN_MAX:
        padding = 6
    else:
        padding = 10
    
    num_bin = bin(num)[2:]
    num_bin = zero_pad(padding, num_bin) + num_bin
    return num_bin


def img_to_b64(img, format=None):
    buffered = BytesIO()
    img.save(buffered, format=format)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def b64_to_img(img_str):
    img_str = base64.b64decode(img_str)
    img_buf = BytesIO(img_str)
    img = Image.open(img_buf)
    return img


def data_to_bin(data):
    if type(data) != type([]):
        raise TypeError("Data must be a list")

    bin_data = ''

    for item in data:
        if item.isalpha():
            bin_data += get_char_bin(item)
        elif item.isnumeric():
            bin_data += get_num_bin(item)
        else:
            raise ValueError("Unsupported data: only alphabets and numbers allowed")
    
    return bin_data


if __name__ == "__main__":
    i= Image.open('bla.bmp')
    ba=i.tobytes()
    print(len(ba))
    print(data_to_bin(['a', 'b', '9']))