from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from cv2 import cv2


def load_image(infilename):
    if infilename[-4:] != '.bmp':
        img = Image.open(infilename)
        infilename = infilename[:-4] + '.bmp'
        img.save(infilename)

    with open(infilename[:-4] + '.bmp', 'rb') as bmp_file:
        bmp = bmp_file.read()
    return bmp, infilename


def load_text(text_path):
    with open(text_path, 'rb') as to_hide_file:
        msg = to_hide_file.read()
    temp = msg.decode('utf-8')
    msg = bytearray(str(len(temp)) + '\n' + temp, 'utf-8')
    msg = [list(map(int, list("00000000"[:8-len(bin(c)[2:])]+bin(c)[2:])))
           for c in msg]
    msg = list(np.array(msg).flatten())
    return msg


def hide_text(image_path, msg):
    bmp, image_path = load_image(image_path)
    start_offset = bmp[10]

    bmpa = bytearray(bmp)
    data_array = load_text(msg)
    assert len(data_array) < len(bmpa) + start_offset

    for i in range(len(data_array)):
        bmpa[i + start_offset] = (bmpa[i + start_offset] -
                                  (bmpa[i + start_offset] % 2)) + data_array[i]

    with open(image_path.replace('.bmp', '_hidden.bmp'), 'wb') as out:
        out.write(bmpa)
    print('\nCover image with secret message saved as original filename'
          ' with "_hidden.bmp" appended\n')

    return bmpa

def unhide_text(image_path):
    with open(image_path, 'rb') as bmp_file:
        bmp = bmp_file.read()

    # color data begins at the byte at position 10
    start_offset = bmp[10]

    arr = [bmp[i] % 2 for i in range(start_offset, len(bmp))]

    # combine our bit array into bytes
    out_bytes = []
    for i in range(0, len(arr), 8):
        if(len(arr) - i > 8):
            temp = arr[i: i + 8]
            out_bytes.append(int("0b"+"".join([str(i) for i in temp]), 2))

    # convert bytes to characters
    out = []
    for b in out_bytes:
        out.append(chr(b))

    output = ''.join(out)
    idx = output.find('\n')
    msg_len = int(output[:idx])
    msg = output[idx + 1: idx + msg_len + 1]
    
    with open("hidden_message.txt", "w") as text_file:
        text_file.write(msg)
    print('Hidden message:')
    print(msg, '\n')
    print('===========================================')
    print('Hidden message saved as "hidden_message.txt"\n')

hide_text('./img/2.jpg', './readme.txt')

unhide_text('./img/2_hidden.bmp')

