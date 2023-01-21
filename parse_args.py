import argparse
import os

MIN_BITS_LEN = 2
MAX_BITS_LEN = 16

def read_args():
    parser = argparse.ArgumentParser()

    # Add required arguments
    parser.add_argument('file', help='Input file path')
    parser.add_argument('-c','--compress', action='store_true', help='compress the file')
    parser.add_argument('-d','--decompress', action='store_true', help='decompress the file')
    parser.add_argument('bit_length', type=int, help='Byte length', nargs='?')

    # Parse arguments
    args = parser.parse_args()

    # Access the arguments
    file = args.file
    compress = args.compress
    decompress = args.decompress
    bit_length = args.bit_length

    if not os.path.isfile(file):
        print("Input file not found.")
        exit(1)
    if not (compress or decompress):
        print("compress or decompress flag should be provided.")
        exit(1)
    if compress and decompress:
        print("only one flag can be provided either compress or decompress.")
        exit(1)
    if decompress and bit_length:
        print("bit_length parameter not needed in decompress mode.")
        exit(1)
    if compress and bit_length is None:
        print("Bit length not provided in compression mode")
        exit(1)
    if compress and not MIN_BITS_LEN <= bit_length <= MAX_BITS_LEN:
        print(f"Bit length should be between {MIN_BITS_LEN} and {MAX_BITS_LEN}.")
        exit(1)
    return file, bit_length, compress, decompress
