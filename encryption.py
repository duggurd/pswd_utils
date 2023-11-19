from codecs import utf_8_encode


def get_key():
    try:
        with open('D:/New Text Document.txt', 'r') as file:
            for row in file:
                key = row
    except:
        msg = 'couldn\'t find key'
        return msg
        
    return key

def xor(x,y):
    out =''
    for x,y in zip(x,y):
        out+=str(int(x)^int(y))
    return out

def bit_stream(data):
    bits = ''
    data = utf_8_encode(data)[0]
    for i in data:
        bits += bin(i).replace('0b','')
    
    prep = bits[0:512] if len(bits) > 512 else f'{bits:0<512}'
    return prep

def encrypt(to_encrypt, key):
    
    to_encrypt = bit_stream(to_encrypt)
    key        = bit_stream(key)

    crypted = xor(to_encrypt, key)

def main():
    key = get_key()
    print(key)

if __name__ == '__main__':
    main()




