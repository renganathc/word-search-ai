from cffi import FFI

ffi = FFI()

ffi.cdef("""

struct Node;

struct Node* create_trie();
void addWordsFromDoc();
struct Node* prefix_search(struct Node* prev_state, char letter, int* wordFound);

""")

lib = ffi.dlopen("libtrie_engine.so")

lib.create_trie()
lib.addWordsFromDoc()

word = "CARDINALL"
prev_state = ffi.NULL
word_found = ffi.new("int*", 0)

for letter in word:
    prev_state = lib.prefix_search(prev_state, letter.encode("ascii"), word_found)
    print(letter, "")
    if word_found[0] == 1:
        print("-word found\n\n")
