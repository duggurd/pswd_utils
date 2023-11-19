from codecs import utf_8_encode

class bit_stream(): 
    
    ''' 
    Usage:
        bit_stream(inp = [str, float, int or list], formatting = ['UTF-8', 'RAW']) -> str
    
    params:
        inp (str, float, int or list): data to convert to bit-stream
        formatting (str): how to interpret different data-types
    
    Returns: 
        str: Bit-stream of input value
    
    '''

    def __init__(self, inp, length = None, input_type = None , formatting = 'UTF-8') -> None:
        '''
        Params:
            [length]: length of final bit stream
            [input_type]: type of the input value
            [inp]: value to convert to bit-stream
            [out]: output
            [formatting]: how to interpret different data-types. 'UTF-8' or 'RAW'
        '''

        self.length = length
        if input_type == None:
            self.input_type = type(inp) 
        else: 
            self.input_type = input_type
        self.formatting = formatting #UTF-8, [U+0020-U+007E]. RAW return pure byte-value of ints/floats, not UTF-8 of character
        self.inp = inp

        self.main()

    def to_bit_stream(self, inp) -> str:
        SUCCESS = 0
        error_msg = 0
        bits = None

        if self.formatting == 'UTF-8':
            UTF_vals = []
            c_stream = ''
            
            if self.input_type == list:
                for i in inp:
                    c_stream += c_stream
            else:
                c_stream = str(inp)
            
            for i in c_stream:
                UTF_vals.append(utf_8_encode(i))
            
            bits = [f'{i:<08}' for i in [f'{int(i):b}' for i in c_stream]]
        
        #Todo: implement RAW format
        elif self.formatting == 'RAW':
            SUCCESS = 0
            error_msg = 'not implemented yet'
            pass

        return bits, error_msg, SUCCESS
    
    def main(self):
        SUCCESS = 0
        
        if self.input_type != int or self.input_type != str or self.input_type != float or self.input_type != list:
            SUCCESS = 1
            error_msg = 'Invalid input type. Input must be str, int, float or list.'
            return self.inp, error_msg, SUCCESS
        
        
        out, err, s = self.to_bit_stream(inp = self.inp, formatting = self.formatting)
        return out, err, s



    