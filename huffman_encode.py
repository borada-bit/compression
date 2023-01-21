from bitarray import bitarray
from bitarray.util import huffman_code
from pprint import pprint
from io_stream import get_frequencies

def huffman_encode(input_file: str, bit_len: int):
    # Create frequency table
    freq, padded_bits = get_frequencies(input_file, bit_len)

    # Create huffman code
    huffman_codes = huffman_code(freq)
    pprint(huffman_codes)
    print(f'Padded bits: {padded_bits}')
    
    encode_file(f'{input_file}.hf', huffman_codes, bit_len)

def encode_file(file_name: str, huffman_codes, bit_len):
    pass