from bitarray import bitarray
from collections import defaultdict

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
        
    return frequency, padded_bits