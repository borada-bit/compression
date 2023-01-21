import argparse
import os

MIN_BITS_READ = 2
MAX_BITS_READ = 16

def read_args():
    parser = argparse.ArgumentParser()

    # Add required arguments
    parser.add_argument('file', help='Input file path')
    parser.add_argument('-c','--compress', action='store_true', help='compress the file')
    parser.add_argument('-d','--decompress', action='store_true', help='decompress the file')
    parser.add_argument('length', type=int, help='Byte length', nargs='?')

    # Parse arguments
    args = parser.parse_args()

    # Access the arguments
    file = args.file
    compress = args.compress
    decompress = args.decompress
    length = args.length

    if not os.path.isfile(file):
        print("Input file not found.")
        exit(1)
    if not (compress or decompress):
        print("compress or decompress flag should be provided.")
        exit(1)
    if compress and not MIN_BITS_READ <= length <= MAX_BITS_READ:
        print(f"Bit length should be between {MIN_BITS_READ} and {MAX_BITS_READ}.")
        exit(1)
    if compress and decompress:
        print("only one flag can be provided either compress or decompress.")
        exit(1)
    if decompress and length:
        print("length parameter not needed in decompress mode.")
        exit(1)
    return file, length, compress, decompress
