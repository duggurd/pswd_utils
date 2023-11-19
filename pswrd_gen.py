import random

def gen_password(length = 64, complexity = 3):

    numbers = '0123456789'
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    uppercase =  'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    symbols = '~`! @#$%^&*()_-+={[}]|\:;"\'<,>.?/'
    
    if complexity == 1:
        plate = numbers + lowercase
    
    elif complexity == 2:
        plate = numbers + lowercase + uppercase
    
    elif complexity == 3:
        plate = numbers + lowercase + uppercase + symbols
    
    pswrd = ''.join([plate[random.randint(0, len(plate) -1 )] for i in range(0, length)])
    
    ops_s = 10e+9
    brute_ops = len(plate)**length
    sec = brute_ops/ops_s
    
    print(
        f'password: {pswrd} \nlength={len(pswrd)} \nbrute_ops={brute_ops:.3e}',
        f'\ncracked in: {sec:.0f}s, {sec/60:.0f}m, {sec/60**2:.0f}h, {sec/(60**2)/24:.1f}d at {ops_s:.0e}')

gen_password()