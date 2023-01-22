from parse_args import read_args
from huffman_encode import huffman_encode
from huffman_decode import huffman_decode

def main():
    # read args 
    input_file, bit_len, compress, decompress = read_args()

    if compress:
        huffman_encode(input_file, bit_len)
    else: 
        huffman_decode(input_file)
 
if __name__ == '__main__':
    main()
