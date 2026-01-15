#ifndef TRIE_H
#define TRIE_H

struct Node;

struct Node* create_trie();
void addWordsFromDoc();
struct Node* prefix_search(struct Node* prev_state, char letter, int* wordFound);

#endif
