from utils import *


def encrypt_lsb(text, msg):
    img = text_to_img(text)
    imsize = img.size

    imgbits = img_to_array(img)
    msgbits = msg_to_bin(msg)

    assert type(msgbits) == type([])
    assert set(msgbits) | {0, 1} == {0, 1}
    assert len(msgbits) <= len(imgbits)

    for i in range(len(msgbits)):
        imgbits[i] = set_lsb(imgbits[i], msgbits[i])
    
    imgbits = np.array(imgbits).reshape((imsize[1], imsize[0]))
    imgbits = np.uint8(imgbits)

    enc_img = Image.fromarray(imgbits, mode="L")

    return enc_img


def decrypt_shre(img):
    img = img_to_array(img)
    
    tag_bits = ''
    for i in range(20):
        tag_bits += str(get_lsb(img[i]))
    
    tag = []
    for i in range(0, 20, 5):
        tag.append(bin_to_char(tag_bits[i : i+5]))
    
    # print(tag)

    msg_len_bits = ''
    for i in range(20, 30):
        msg_len_bits += str(get_lsb(img[i]))
    
    msg_len = int(msg_len_bits, 2)

    # print(msg_len)

    msg_bits = ''
    for i in range(30, 30 + 10*msg_len):
        msg_bits += str(get_lsb(img[i]))
    
    # print(msg_bits, len(msg_bits))
    
    msg = []
    for i in range(0, len(msg_bits), 10):
        msg.append(int(msg_bits[i : i+10], 2))
    
    return msg

if __name__ == "__main__":

    filename = 'enc.bmp'

    text = 'the subtle art of not giving fucks'
    msg = ['s', 'h', 'r', 'e', '3', '2', '6', '1']

    img = encrypt_lsb(text, msg)
    img.save(filename)

    img = Image.open(filename)
    ib64 = img_to_b64(img, format="BMP")
    print(ib64)
    