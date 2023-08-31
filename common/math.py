import base64

v = {
    "bk0": "@#!@@@##$$@@",
    "bk1": "^^#@@!!@#!$",
    "bk2": "@!^^!@#@@$$$$$",
    "bk3": "^^^^^^##@",
    "bk4": "$$$####!!!!!!!"
}

file3_separator = "//_//"

def b1(string):
    encoded_str = string.encode('utf-8')
    b64_encoded = base64.b64encode(encoded_str)
    return b64_encoded.decode()

def b2(string):
    b64_decoded = base64.b64decode(string)
    decoded_str = b64_decoded.decode('utf-8')
    return decoded_str.replace('%00', '')

def decrypt(x):
    a = x[2:]
    for i in range(4, -1, -1):
        key = "bk" + str(i)
        if v.get(key):
            if v[key] != "":
                a = a.replace(file3_separator + b1(v[key]), "")

    try:
        a = b2(a)
        return a, x[:2]
    except Exception as e:
        print(e)
        return "", x[:2]
    
def b1_r(string):
    return string.replace(file3_separator, "")

def b2_r(string):
    encoded_str = string.encode('utf-8')
    b64_encoded = base64.b64encode(encoded_str)
    return b64_encoded.decode()

def encrypt(x, prefix):
    try:
        a = b2_r(x)
        
        for i in range(4, -1, -1):
            key = "bk" + str(i)
            if v.get(key):
                if v[key] != "":
                    a = a.replace(b1_r(v[key]), file3_separator + b1_r(v[key]))
        
        return prefix + a
    except Exception as e:
        print(e)
        return prefix