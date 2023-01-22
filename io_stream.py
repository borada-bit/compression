from bitarray import bitarray
from collections import defaultdict
import pickle
from pprint import pprint

# this is 1024 bytes at a time
CHUNK_SIZE = 1024

# read file for the first time and return frequencies and padding
def get_frequencies_from_file(input_file: str, bit_len: int, log=False):
    frequency = defaultdict(int)
    # workaround to read whole bytes according to bit_len (only need to pad the last bits)
    bytes_to_read = CHUNK_SIZE
    while bytes_to_read * 8 % bit_len != 0:
        bytes_to_read += 1
    assert(bytes_to_read*8 % bit_len == 0)
    if log:
        print(f'{bytes_to_read=}')
    
    padded_bits = []

    with open(input_file, 'rb') as f:
        while True:
            bytes = f.read(bytes_to_read)
            if not bytes:
                break

            bits = bitarray()
            bits.frombytes(bytes)

            # adding padding
            if len(bytes) < bytes_to_read and (len(bytes) * 8) % bit_len != 0:
                padded_bits = [0] * (bit_len - (len(bits) % bit_len))
                if log:
                    print(f'Padding bits {padded_bits}')
                bits.extend(padded_bits)

            # iterate over bitarray in chunks of bit_length
            for i in range(0, len(bits), bit_len):
                chunk = bits[i:i+bit_len]
                if log:
                    print(f'{chunk=}')
                # get string representation
                value = chunk.to01()
                frequency[value] += 1

            print(f"File bits: {bits}")
        
    return frequency, padded_bits

def write_hf_code_to_file(input_file, output_file, hf_code, bit_len):
    print(f'compressing file.. ')
    bytes_to_write = CHUNK_SIZE
    while bytes_to_write * 8 % bit_len != 0:
        bytes_to_write += 1
    assert(bytes_to_write*8 % bit_len == 0)  
    
    bytes_to_read = bytes_to_write
    with open(input_file, 'rb') as f:
        while True:
            bytes = f.read(bytes_to_read)
            if not bytes:
                break

            bits = bitarray()
            bits.frombytes(bytes)

            # adding padding
            # if this is the last chunk and it does not contain 8bits or something like that
            ### NOT SURE IF THIS IS THE NEEDED PADDDING PART
            if len(bytes) < bytes_to_read and (len(bytes) * 8) % bit_len != 0:
                padded_bits = [0] * (bit_len - (len(bits) % bit_len))
                bits.extend(padded_bits)

            encoded = bitarray()
            # iterate over bitarray in chunks of bit_length
            for i in range(0, len(bits), bit_len):
                chunk = bits[i:i+bit_len]
                # get string representation
                value = chunk.to01()
                # Encode data from hf_codes table
                encoded.extend(hf_code[value])
            
            ### PROBABLY needs reworking with large files because of chunks
            # from hexdumps it writes to 2 byte address and start at the end of byte so if we have 1010111 -> Hexdump addr 0 : 00af
            # maybe no need to look into hexdump and just try to read the data from the file, not sure about padding
            # bits at the end are written to the next 2 byte address starting at the start of second byte? xx1 -> 0080
            # meaning that 0 are padded automatically for us but not sure what happens when reading
            # 0 are ignored and all is good? probabbly because they dont influence the value when padded at the back
            print(f"Encoded bits: {encoded}")
            with open(output_file, 'ab') as of:
                encoded.tofile(of)
    pass

            
def decode_file(file_name):
    with open(f'{file_name}.hf', 'rb') as f:
        # read header -> huffman code table
        header = pickle.load(f)
        pprint(header)
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
        
        while True:
            bytes = f.read(bytes_to_read)
            if not bytes:
                break

            bits = bitarray()
            # retrieve encoded bits
            bits.frombytes(bytes)

            print(f"Encoded bits: {bits}")

            value = bitarray()
            for bit in bits:
                # probably not efficient
                value.extend([bit])
                # print(f"Currently have {value}")
                original_value = header.get(value.to01())
                # print(f'Received original value {original_value}')
                if original_value and symbol_translated_count < symbol_count:
                    symbol_translated_count += 1
                    value.clear()
                    original_bits.extend(original_value)
            
        # Only remove if this is the last chunk?
        if header['padded_bits']:
            # remove padded bits
            original_bits = original_bits[:-header['padded_bits']]
        print(f'Decompressed file chunk in bits:\n{original_bits}')

        with open('output', 'wb') as of:
            original_bits.tofile(of)
    pass
