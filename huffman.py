from parse_args import read_args


def main():
    # read args 
    input_file, bit_len, compress, decompress = read_args()

def encode_table(node, code=''):
    combined_code = code + str(node.huff)
 
    if node.left:
        encode_table(node.left, combined_code)
    if node.right:
        encode_table(node.right, combined_code)
 
    if not node.left and not node.right:
        encoded_huffman[node.symbol] = combined_code 

class Huffman:
    def __init__(self):
        pass

def main():
    bytes_to_read = 1
    assert len(sys.argv) == 2

    frequency = defaultdict(int)
    file_name = sys.argv[1]
    # Read text as bytes
    with open(file_name, 'rb') as f:
        while True:
            byte = f.read(bytes_to_read)
            if not byte:
                break
            frequency[byte] += 1

    # Insert values into heap
    heap = []
    for c in frequency:
        heapq.heappush(heap, Node(c, frequency[c]))

    # HUFFMAN CODING
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        left.huff = 0
        right.huff = 1

        combined_node = Node(left.symbol+right.symbol, left.freq+right.freq, left=left, right=right)
        combined_node = Node(left.symbol+right.symbol, left.freq+right.freq, left=left, right=right)
        heapq.heappush(heap, combined_node)

    # One node has all combined info
    encode_table(heap[0])
    # Encoded table
    pprint(encoded_huffman)

    # Testing to see how does encoded string looks like
    encoded_str = ""
    with open(file_name, 'rb') as f:
        while True:
            byte = f.read(bytes_to_read)
            if not byte:
                break
            encoded_str += encoded_huffman[byte] + "|"
    
    print(encoded_str)
    
    # Write to file compressed text and decompressing table/info
    pass

if __name__ == '__main__':
    main()
