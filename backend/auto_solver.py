import os
from cffi import FFI

ffi = FFI()

ffi.cdef("""

struct Node;

struct Node* create_trie();
void addWordsFromDoc();
struct Node* prefix_search(struct Node* prev_state, char letter, int* wordFound);

""")

HERE = os.path.dirname(os.path.abspath(__file__)) #for docker containers
lib = ffi.dlopen(HERE + "/libtrie_engine.so")

lib.create_trie()
lib.addWordsFromDoc()

def linear_chain_search(crossword: list[list[str]], dir: tuple[int], start_index: tuple[int], coordinates: list[tuple[int]]):
    prev_state = ffi.NULL
    word_found = ffi.new("int*", 0)

    idx = list(start_index)

    while True:
        if idx[0] < 0 or idx[0] > len(crossword) - 1 or idx[1] < 0 or idx[1] > len(crossword[0]) - 1:
            break
        letter = crossword[idx[0]][idx[1]]
        prev_state = lib.prefix_search(prev_state, letter.encode("ascii"), word_found)
        if word_found[0] == 1:
            coordinates.append([start_index, (idx[0], idx[1])])
            # for i in range(max(abs(idx[0] - start_index[0]), abs(idx[1] - start_index[1])) + 1):
            #     print(crossword[start_index[0] + i*dir[0]][start_index[1] + i*dir[1]], end="")
            # print("")
            break
        if prev_state == ffi.NULL:
            break
        idx[0] += dir[0]
        idx[1] += dir[1]

def auto_find_words(crossword: list[list[str]]) -> list:

    coordinates = list()
    search_dir = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

    for i in range(len(crossword)):
        for j in range(len(crossword[0])):
            for dir in search_dir:
                linear_chain_search(crossword, dir, (i, j), coordinates)

    print (len(coordinates), "words found by find_words")
    return coordinates

# crossword = [['G', 'A', 'R', 'D', 'E', 'N', 'Y', 'S', 'M', 'B', 'M', 'T', 'O', 'L', 'S'], ['N', 'I', 'A', 'R', 'M', 'E', 'L', 'E', 'S', 'E', 'E', 'R', 'W', 'O', 'U'], ['U', 'C', 'I', 'N', 'C', 'I', 'P', 'E', 'A', 'S', 'I', 'A', 'M', 'S', 'N'], ['L', 'M', 'L', 'I', 'N', 'O', 'I', 'T', 'A', 'C', 'A', 'V', 'R', 'P', 'S'], ['P', 'O', 'P', 'S', 'I', 'C', 'L', 'E', 'O', 'L', 'D', 'E', 'K', 'I', 'H'], ['U', 'I', 'P', 'E', 'C', 'A', 'M', 'P', 'I', 'O', 'O', 'L', 'F', 'C', 'I'], ['Y', 'T', 'N', 'S', 'R', 'E', 'T', 'L', 'M', 'D', 'N', 'T', 'R', 'E', 'N'], ['P', 'W', 'N', 'S', 'O', 'E', 'P', 'A', 'T', 'G', 'N', 'E', 'D', 'X', 'E'], ['A', 'U', 'G', 'R', 'I', 'A', 'D', 'Y', 'B', 'O', 'A', 'Y', 'A', 'T', 'E'], ['R', 'L', 'J', 'U', 'L', 'Y', 'G', 'R', 'S', 'A', 'S', 'O', 'U', 'P', 'A'], ['K', 'E', 'F', 'G', 'L', 'C', 'E', 'A', 'T', 'H', 'I', 'R', 'G', 'A', 'S'], ['B', 'A', 'L', 'Y', 'P', 'A', 'E', 'N', 'O', 'C', 'R', 'E', 'U', 'R', 'D'], ['S', 'H', 'O', 'R', 'T', 'S', 'O', 'O', 'H', 'A', 'E', 'H', 'S', 'H', 'R'], ['U', 'Y', 'P', 'E', 'M', 'N', 'O', 'S', 'A', 'E', 'S', 'S', 'T', 'D', 'E'], ['C', 'H', 'E', 'T', 'A', 'M', 'C', 'L', 'Y', 'B', 'G', 'M', 'R', 'E', 'S'], ['X', 'L', 'A', 'O', 'V', 'Z', 'R', 'C', 'O', 'J', 'B', 'R', 'I', 'N', 'S'], ['F', 'O', 'S', 'E', 'M', 'A', 'E', 'R', 'C', 'E', 'C', 'I', 'O', 'W', 'L'], ['B', 'L', 'O', 'S', 'S', 'U', 'M', 'M', 'E', 'R', 'W', 'B', 'M', 'O', 'S']]
# auto_find_words(crossword)
