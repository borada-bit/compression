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
    encode_file(input_file, huffman_codes, bit_len, padded_bits)

def encode_file(input_file: str, huffman_codes, bit_len, padded_bits):
    # reverse dictionary for later decompression usage, but compress using original
    header_dict = {(value.to01()):key for (key,value) in huffman_codes.items()}
    # save for decompression
    header_dict['bit_len'] = bit_len
    header_dict['padded_bits'] = len(padded_bits)
    serialized_huffman_codes = pickle.dumps(header_dict)
    with open(f'{input_file}.hf', 'wb') as f:
        f.write(serialized_huffman_codes)

    # write codes
    io_stream.write_hf_code_to_file(input_file, f'{input_file}.hf', huffman_codes, bit_len)
    pass
