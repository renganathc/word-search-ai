#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Node {
    struct Node* children[26];
    int isWord; // my bool
};

struct Node* root = NULL;

struct Node* new_node(int isWord) {
    struct Node* node = (struct Node*)malloc(sizeof(struct Node));
    node->isWord = isWord;
    for (int i = 0; i < 26; i++) {
        node->children[i] = NULL;
    }
    return node;
}

struct Node* create_trie() {
    root = new_node(0);
    return root;
}

void insert_node(struct Node** prev, char letter, int isWord) {
    if (!(*prev)->children[(int)letter-65]) {
        struct Node* node = new_node(isWord);
        (*prev)->children[(int)letter-65] = node;
    }

    *prev = (*prev)->children[(int)letter-65];
}

void addWord(char* word) {
    int length = strlen(word);
    struct Node* prev = root;
    for(int i = 0; i<length; i++) {
        insert_node(&prev, *(word+i), 0);
    }
    prev->isWord = 1;
}

void addWordsFromDoc() {
    
}

struct Node* prefix_search(struct Node* prev_state, char letter) {
    if (!prev_state) prev_state = root;
    if (prev_state->children[(int)letter - 65]) {
        return prev_state->children[(int)letter - 65];
    } else {
        return NULL;
    }
}

// usage : if(prefix_search(prev_state, 'a') != NULL) { YAY, CHECK WHETHER isWord is 1 and call it a day or continue or do whatever you wan t}

int main() {
    create_trie();
}


