from bitarray import bitarray
from bitarray.util import huffman_code
from pprint import pprint
import io_stream
import pickle

def huffman_encode(input_file: str, bit_len: int):
    # Create frequency table
    freq, padded_bits = io_stream.get_frequencies_from_file(input_file, bit_len)

    # Create huffman code
    huffman_codes = huffman_code(freq)
    pprint(huffman_codes)
    print(f'Padded bits: {padded_bits}')
    
    # Encode to file
    encode_file(input_file, huffman_codes, bit_len)

def encode_file(input_file: str, huffman_codes, bit_len):
    # ADD header
    serialized_huffman_codes = pickle.dumps(huffman_codes)

    with open(f'{input_file}.hf', 'wb') as f:
        f.write(serialized_huffman_codes)

    # write codes
    encode_file(f'{input_file}.hf', huffman_codes, bit_len)

    # ADD padded bits information
    pass
