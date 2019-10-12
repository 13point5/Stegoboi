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


if __name__ == "__main__":
    text = 'the subtle art of not giving fucks'
    msg = list('387653v78b56y')

    img = encrypt_lsb(text, msg)
    img.save('enc.jpg')