from bitarray.util import huffman_code
from pprint import pprint
import io_stream
import pickle

def huffman_encode(input_file: str, bit_len: int):
    # Create frequency table
    freq, padded_bits = io_stream.get_frequencies_from_file(input_file, bit_len)

    # Create huffman code
    symbol_count = 0
    for val in freq.values():
        symbol_count += val
        
    huffman_codes = huffman_code(freq)
    
    # Encode to file
    encode_file(input_file, huffman_codes, bit_len, padded_bits, symbol_count)

def encode_file(input_file: str, huffman_codes, bit_len, padded_bits, symbol_count):
    # reverse dictionary for later decompression usage, but compress using original
    header_dict = {(value.to01()):key for (key,value) in huffman_codes.items()}
    # save for decompression
    header_dict['bit_len'] = bit_len
    header_dict['padded_bits'] = len(padded_bits)
    header_dict['symbol_count'] = symbol_count
    pprint(header_dict)
    serialized_huffman_codes = pickle.dumps(header_dict)
    with open(f'{input_file}.hf', 'wb') as f:
        f.write(serialized_huffman_codes)

    # write codes
    io_stream.write_hf_code_to_file(input_file, f'{input_file}.hf', huffman_codes, bit_len)
    pass
