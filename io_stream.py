from bitarray import bitarray
from collections import defaultdict
import pickle
from pprint import pprint
import time

CHUNK_SIZE = 1#1024*1024*30 # megabytes

# read file for the first time and return frequencies and padding
def get_frequencies_from_file(input_file: str, bit_len: int):
    frequency = defaultdict(int)
    # workaround to read whole bytes according to bit_len (only need to pad the last bits)
    bytes_to_read = CHUNK_SIZE
    while bytes_to_read * 8 % bit_len != 0:
        bytes_to_read += 1
    assert(bytes_to_read*8 % bit_len == 0)
    
    padded_bits = []

    with open(input_file, 'rb') as f:
        while True:
            bytes = f.read(bytes_to_read)
            if not bytes:
                break

            bits = bitarray()
            bits.frombytes(bytes)

            # adding padding to last bytes
            if len(bytes) < bytes_to_read and (len(bytes) * 8) % bit_len != 0:
                padded_bits = [0] * (bit_len - (len(bits) % bit_len))
                bits.extend(padded_bits)
            
            # convert all bits to long string for optimisation
            bits_str = bits.to01()
            # start = time.time()
            # iterate over bitarray in chunks of bit_length
            for i in range(0, len(bits), bit_len):
                chunk = bits_str[i:i+bit_len]
                frequency[chunk] += 1
            # print(f'Time taken {time.time() - start}')    
    return frequency, padded_bits

def write_hf_code_to_file(input_file, output_file, hf_code, bit_len):
    print(f'compressing file.. ')
    bytes_to_write = CHUNK_SIZE
    while bytes_to_write * 8 % bit_len != 0:
        bytes_to_write += 1
    assert(bytes_to_write*8 % bit_len == 0)  
    
    bytes_to_read = bytes_to_write
    with open(input_file, 'rb') as f:
        encoded = bitarray()
        while True:
            bytes = f.read(bytes_to_read)
            if not bytes:
                break
            bits = bitarray()
            bits.frombytes(bytes)

            ### NOT SURE IF THIS IS THE NEEDED PADDDING PART
            if len(bytes) < bytes_to_read and (len(bytes) * 8) % bit_len != 0:
                padded_bits = [0] * (bit_len - (len(bits) % bit_len))
                bits.extend(padded_bits)

            bits_str = bits.to01()
            for i in range(0, len(bits), bit_len):
                chunk = bits_str[i:i+bit_len]
                encoded.extend(hf_code[chunk])
            
        with open(output_file, 'ab') as of:
            encoded.tofile(of)
    pass

            
def decode_file(file_name):
    original_bits = bitarray()
    with open(f'{file_name}.hf', 'rb') as f:
        # read header -> huffman code table
        header = pickle.load(f)
        # pprint(header)
        bit_len = header['bit_len']
        if header['padded_bits']:
            print(f"{header['padded_bits']=}")
        
        symbol_count = header['symbol_count']        
        symbol_translated_count = 0
        
        bytes_to_read = CHUNK_SIZE
        while bytes_to_read * 8 % bit_len != 0:
            bytes_to_read += 1
        assert(bytes_to_read*8 % bit_len == 0)

        original_bits = bitarray()
        start = bitarray()
        start_t = time.time()
        while True:
            bytes = f.read(bytes_to_read)
            if not bytes:
                break

            bits = bitarray()
            bits.extend(start)
            # clear this one so only new data is extended every loop
            start.clear()
            # retrieve encoded bits
            bits.frombytes(bytes)
            # convert bits to string for optimisation
            bits_str = bits.to01()

            value = ""
            for bit in bits_str:
                value += bit
                original_value = header.get(value)
                if original_value and symbol_translated_count < symbol_count:
                    symbol_translated_count += 1
                    value = ""
                    original_bits.extend(original_value)
            start.extend([int(b) for b in value])
        print(f"Time taken to decompress {time.time() - start_t}")
        if header['padded_bits']:
            # remove padded bits
            original_bits = original_bits[:-header['padded_bits']]

    with open('output', 'wb') as of:
        original_bits.tofile(of)
    pass
