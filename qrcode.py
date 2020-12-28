# Codage alpha-numérique


def alphanumeric_encode(msg):
    bytes = []
    divided = [msg[i:i+2] if i+2 <= len(msg) else msg[i:i+1]
               for i in range(0, len(msg), 2)]
    for pair in divided:
        if len(pair) >= 2:
            bits = bin((int(pair[0], 36)*45) + int(pair[1], 36))[2:]
        else:
            bits = bin((int(pair, 36)))[2:]
        while len(bits) < 11:
            bits = "0" + bits
        bytes.append(bits)
    return " ".join(bytes)

# Préparation du code


def prepare_code(msg, mode):
    alpha = alphanumeric_encode(msg)
    size_indicator = bin(len(msg))[2:]
    while len(size_indicator) < 9:
        size_indicator = "0" + size_indicator
    return "{} {} {}".format(mode, size_indicator, alpha)

# Remplissage du code


def fill_code(msg, mode, max):
    res = prepare_code(msg, mode)
    code = res.replace(" ", "")
    if len(code) < 152:
        code += "0000"
        res += " 0000"
    while len(code) % 8 != 0:
        code += "0"
        res += "0"

    pad_length = (max-len(code))//8
    for i in range(pad_length):
        if i % 2 == 0:
            res += " 11101100"
            code += "11101100"
        else:
            res += " 00010001"
            code += "00010001"
    return res

# Détermination des coefficients


def msg_coeffs(msg, mode, max):
    filled_msg = fill_code(msg, mode, max).replace(" ", "")
    divided = [filled_msg[i:i+8] for i in range(0, len(filled_msg), 8)]
    coeffs = [str(int(word, 2)) for word in divided]

    return ",".join(coeffs)


# Détermination du polynome grâce aux coefficients
def coeffs_poly(coeffs):
    res = ""
    splitted = coeffs.split(",")
    for i, coeff in enumerate(splitted):
        res += "{}x^({})".format(coeff, len(splitted)-i-1)
        if i != len(splitted)-1:
            res += "+"
    return res


def coded_msg(msg, mode, max, correction):
    filled = fill_code(msg, mode, max)
    for word in correction:
        word_filled = bin(word)[2:]
        while len(word_filled) < 8:
            word_filled = "0" + word_filled
        filled += " {}".format(word_filled)
    return filled
