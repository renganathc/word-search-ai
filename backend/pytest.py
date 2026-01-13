from cffi import FFI

ffi = FFI()

ffi.cdef("""

struct Node;

struct Node* create_trie();
void addWordsFromDoc(char* word);
struct Node* prefix_search(struct Node* prev_state, char letter);

""")

lib = ffi.dlopen("./libtrie.so")

lib.create_trie()
lib.addWordsFromDoc()

