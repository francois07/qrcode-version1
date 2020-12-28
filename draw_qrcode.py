from qrcode import coded_msg
from PIL import Image, ImageFont, ImageDraw, ImageEnhance

MSG = "MATHSDISCRETES"
MODE = "0010"
MAX = 19*8
CORRECTION = [211, 212, 181, 2, 31, 139, 106]


def draw_pattern(qrcode, x, y):
    draw = ImageDraw.Draw(qrcode)
    draw.rectangle(
        [(x, y), (x+6, y+6)], outline="black", width=1)
    draw.rectangle(
        [(x, y), (x+6, y+6)], outline="black", width=1)
    draw.rectangle(
        [(x+2, y+2), (x+4, y+4)], outline="black", fill="black", width=1)


def draw_timing(qrcode):
    for i in range(7, 13):
        color = (0, 0, 0) if i % 2 == 0 else (255, 255, 255)
        qrcode.putpixel((i, 6), color)
        qrcode.putpixel((6, i), color)


def draw_dark_module(qrcode):
    qrcode.putpixel((8, 4*1+9), (0, 0, 0))


def zigzag(col, start, end):
    res = []
    j = start
    k = 1
    if start > end:
        while j >= end:
            k = (k+1) % 2
            res.append((col-k, j))
            if k != 0:
                j -= 1
    else:
        while j <= end:
            k = (k+1) % 2
            res.append((col-k, j))
            if k != 0:
                j += 1
    return res


def apply_mask(bit, mask, row, column):
    if mask == -1:
        return bit
    elif mask == 0:
        if (row+column) % 2 == 0:
            return 1 if bit == 0 else 0
    elif mask == 1:
        if (row) % 2 == 0:
            return 1 if bit == 0 else 0
    elif mask == 2:
        if (column) % 3 == 0:
            return 1 if bit == 0 else 0
    elif mask == 3:
        if (row + column) % 3 == 0:
            return 1 if bit == 0 else 0
    elif mask == 4:
        if (row // 2 + column // 3) % 2 == 0:
            return 1 if bit == 0 else 0
    elif mask == 5:
        if ((row * column) % 2) + ((row * column) % 3) == 0:
            return 1 if bit == 0 else 0
    elif mask == 6:
        if (((row * column) % 2) + ((row * column) % 3)) % 2 == 0:
            return 1 if bit == 0 else 0
    elif mask == 7:
        if (((row + column) % 2) + ((row * column) % 3)) % 2 == 0:
            return 1 if bit == 0 else 0
    return bit


def draw_column(data, qrcode, col, start, end, mask):
    coords = zigzag(col, start, end)
    modules_coords = zigzag(20, 20, 14) + [(20, 13)]
    for i, p in enumerate(coords):
        value = apply_mask(int(data[i]), mask, p[1], p[0]) if (
            p[0], p[1]) not in modules_coords else int(data[i])
        color = (0, 0, 0) if value == 1 else (255, 255, 255)
        qrcode.putpixel(p, color)
    return i+1


def draw_data(msg, qrcode, mask):
    z = 0
    raw = coded_msg(msg, MODE, MAX, CORRECTION)
    coded = raw.replace(" ", "")
    z += draw_column(coded, qrcode, 20, 20, 9, mask)
    z += draw_column(coded[z:], qrcode, 18, 9, 20, mask)
    z += draw_column(coded[z:], qrcode, 16, 20, 9, mask)
    z += draw_column(coded[z:], qrcode, 14, 9, 20, mask)
    z += draw_column(coded[z:], qrcode, 12, 20, 7, mask)
    z += draw_column(coded[z:], qrcode, 12, 5, 0, mask)
    z += draw_column(coded[z:], qrcode, 10, 0, 5, mask)
    z += draw_column(coded[z:], qrcode, 10, 7, 20, mask)
    z += draw_column(coded[z:], qrcode, 8, 12, 9, mask)
    z += draw_column(coded[z:], qrcode, 5, 9, 12, mask)
    z += draw_column(coded[z:], qrcode, 3, 12, 9, mask)
    z += draw_column(coded[z:], qrcode, 1, 9, 12, mask)


def draw_infos(qrcode, mask):
    if mask == -1:
        return
    info_strings = ["111011111000100", "111001011110011", "111110110101010", "111100010011101",
                    "110011000101111", "110001100011000", "110110001000001", "110100101110110"]
    bits = info_strings[mask]
    j = 0
    for i in range(8):
        if i == 6:
            continue
        color = (0, 0, 0) if int(bits[j]) == 1 else (255, 255, 255)
        qrcode.putpixel((i, 8), color)
        j += 1
    for i in range(8, -1, -1):
        if i == 6:
            continue
        color = (0, 0, 0) if int(bits[j]) == 1 else (255, 255, 255)
        qrcode.putpixel((8, i), color)
        j += 1
    j = 0
    for i in range(20, 13, -1):
        color = (0, 0, 0) if int(bits[j]) == 1 else (255, 255, 255)
        qrcode.putpixel((8, i), color)
        j += 1
    for i in range(13, 21):
        color = (0, 0, 0) if int(bits[j]) == 1 else (255, 255, 255)
        qrcode.putpixel((i, 8), color)
        j += 1


def draw_qrcode(filename="qrcode", msg=MSG, mask=-1, size=250):
    qrcode = Image.new('RGB', (21, 21), "white")

    draw_pattern(qrcode, 0, 0)
    draw_pattern(qrcode, 21-1-6, 0)
    draw_pattern(qrcode, 0, 21-1-6)

    draw_timing(qrcode)

    draw_dark_module(qrcode)
    draw_data(MSG, qrcode, mask)

    draw_infos(qrcode, mask)
    new_img = qrcode.resize((size, size))
    new_img.save("images/{}.png".format(filename))
    return new_img


imgs = []

for i in range(-1, 8):
    img = draw_qrcode(filename="qrcode_mask{}".format(i), mask=i, size=250)
    imgs.append(img)

final = Image.new('RGB', (860, 200), "white")
draw = ImageDraw.Draw(final)
for i, img in enumerate(imgs):
    new_img = img.resize((80, 80))
    final.paste(new_img, (30+i*90, 36))
    text = "masque {}".format(i-1) if i != 0 else "Aucun\nmasque"
    draw.text((45+i*90, 130), text, (0, 0, 0),
              font=ImageFont.truetype("arial.ttf"))
final.save("images/final.png")
