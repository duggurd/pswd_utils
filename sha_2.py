# SHA-256

from codecs import utf_8_decode, utf_8_encode
from string import hexdigits

def bit_stream(val):
    
    bits =''
    for char in val:
        byte = utf_8_encode(char)[0]
        for n in byte: 
            bits += f'{n:>08b}'
    return bits

def padding(inp):
    
    bits = bit_stream(inp)

    l_msg = f'{len(bits):b}' #l -> length of message (64 bits reserved)
    l_msg = f'{l_msg:>064}'
    bits_to_pad = 512 - len(bits) - len(l_msg)

    #start padding
    bits += '1' #start by adding one to the bit-stream
    bits += '0' * (bits_to_pad - 1) #-1 because of above operation
    bits += l_msg #add len of message
    
    return bits

def find_primes(n):
    primes = []
    i=2
    
    while len(primes)< n:
        max_div = int(i**(1/2))
        prime = False

        for a in range(2, 2 + max_div):
            if i != a  and i % a == 0:
                prime = False
                break
            prime = True

        if prime:
            primes.append(i)
        i+=1

    return primes

def constants(n = 64):
    
    primes = find_primes(n)
    constants = [f'{int(i.split(".")[1]):b}' for i in [f'{prime**(1/3):0.16f}' for prime in primes]]
    constants = [f'{i:.32s}' for i in constants]
    return constants

def shr(bits:str, n:int):

    bits = f'{bits:0>{len(bits)+n}}'
    bits = bits [:32]

    return bits

def rotr(bits:str, n:int):

    shift = bits [len(bits)-n: len(bits)]
    shift += bits
    bits = shift [:len(bits)]

    return bits

def xor(x, y):
    out=''
    for i in range(len(x)):
        if (x[i] == '1' and y[i] == '1') or (x[i] == '0' and y[i] == '0'):
            out += '0'
        elif x[i] == '1' or y[i] == '1':
            out += '1'
    
    bits = out
    
    return bits

def add(x, y):
    out = f'{(int(x, base = 2) + int(y, base = 2)):0>32b}'
    bits = out[len(out)-len(x):]

    return bits

def choice(x,y,z):
    
    out=''
    for i in range(len(x)):
        if x[i] == '0':
            out+=z[i]
        elif x[i] == '1':
            out+=y[i]
    bits = out

    return bits

def majority(x,y,z):
    
    out=''
    for i in range(len(x)):
        step=''
        step = x[i] + y[i] + z[i]

        if str(step).count('0') > str(step).count('1'):
            out += '0'
        
        else: 
            out += '1'
    bits = out

    return bits
    
def sigma0(bits):
    op1 = rotr(bits, 7)
    op2 = rotr(bits, 18)
    op3 = shr(bits, 3)
    
    bits = xor(xor(op1, op2), op3)
    return bits

def sigma1(bits):
    op1 = rotr(bits, 17)
    op2 = rotr(bits, 19)
    op3 = shr(bits, 10)

    bits = xor(xor(op1, op2), op3)
    return bits

def sigma3(bits):
    op1 = rotr(bits, 2)
    op2 = rotr(bits, 13)
    op3 = rotr(bits, 22)

    bits = xor(xor(op1, op2), op3)
    return bits

def sigma4(bits):
    op1 = rotr(bits, 6)
    op2 = rotr(bits, 11)
    op3 = shr(bits, 25)

    bits = xor(xor(op1, op2), op3)
    return bits

def words(inp):

    bits = padding(inp)
    words = []
    n_words = int(len(bits)/32)
    for i in range(n_words):
        words.append(bits[32*i:32*(i+1)])

    while len(words) < 64:
        w0 = words[-16]
        w1 = sigma0(words[-15])
        w2 = words[-7]
        w3 = sigma1(words[-2])       
    
        op1 = add(w0, w1)
        op2 = add(op1, w2)
        op3 = add(op2, w3)
        
        words.append(op3)
    
    return words


def init_hash(inp):
    
    h = '0.'
    init_hash = []
    primes = find_primes(8)
    
    for i in primes:
        op1 = str(i**(1/2)).split('.')[1]
        op2 = float(h+op1) * (2**32)
        op3 = int(op2)

        init_hash.append(f'{op3:0>32b}')

    return init_hash


def temp(inp):
    initial = init_hash(inp)
    block = initial
    w = words(inp)
    k = constants()
    
    for i in range(len(w)):
    
        op1 = choice(block[-4], block[-3], block[-2])
        op2 = sigma4(block[-4])
        op3 = block[-1]

        temp0 = add(add(add(add(w[i], k[i]), op1),op2), op3)
        
        op1 = majority(block[0], block[1], block[2])
        op2 = sigma3(block[0])
        temp1 = add(op1,op2)

        block.insert(0, add(temp0,temp1))
        block = block[0:-1]
        block[-4] = temp1
    
    final_block = [add(a, b) for a, b in zip(initial, block)]
    return final_block

    
def decode(inp):
    final_hash = temp(inp)
    hexstring = []
    for item in final_hash:
        hexadec = (f'{int(item, base =2):x}')
        hexstring.append(str(hexadec))
    
    for bits, hexa in zip(final_hash, hexstring):
        print(bits + ': ' + hexa)

    concat = ''.join(hexstring)
    return concat


def sha_2(val = ''):
    
    sha_2_sum = decode(val)
    print('\n' + 'final hash:' + '\n' + sha_2_sum)
    
    return sha_2_sum

sha_2()