#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "trie_engine.h"

struct Node {
    struct Node* children[26];
    int isWord; // my bool
};

struct Node* root = NULL;

struct Node* new_node() {
    struct Node* node = (struct Node*)malloc(sizeof(struct Node));
    node->isWord = 0;
    for (int i = 0; i < 26; i++) {
        node->children[i] = NULL;
    }
    return node;
}

struct Node* create_trie() {
    root = new_node();
    return root;
}

void insert_node(struct Node** prev, char letter) {
    if (!(*prev)->children[(int)letter-65]) {
        struct Node* node = new_node();
        (*prev)->children[(int)letter-65] = node;
    }

    *prev = (*prev)->children[(int)letter-65];
}

void addWord(char* word) {
    int length = strlen(word);
    struct Node* prev = root;
    for(int i = 0; i<length; i++) {
        insert_node(&prev, *(word+i));
    }
    prev->isWord = 1;
}

void addWordsFromDoc() {
    char buffer[50];
    //FILE* fp = fopen("english-words.txt", "r");
    FILE* fp = fopen("words_alpha.txt", "r");
    if (!fp) {
        perror("Failed to open file");
        return;
    }
    int count = 0;
    while (fgets(buffer, sizeof(buffer), fp)) {
        buffer[strcspn(buffer, "\r\n")] = 0;
        if(strlen(buffer) < 4) continue;
        for (int i = 0; buffer[i]; i++) {
            if (buffer[i] >= 'a' && buffer[i] <= 'z') {
                buffer[i] -= 32;
            }
        }
        addWord(buffer);
        count++;
    }
    fclose(fp);
    printf("Added %d words into prefix tree\n\n", count);
}

struct Node* prefix_search(struct Node* prev_state, char letter) {
    if (!prev_state) {
        prev_state = root;
    }
    if (prev_state->children[(int)letter - 65]) {
        return prev_state->children[(int)letter - 65];
    } else {
        return NULL;
    }
}

// int main() {
//     create_trie();
//     addWordsFromDoc();
//     char test_word[20] = "TESTING";
//     int length = strlen(test_word);

//     struct Node* state = NULL;
//     int found = 1;

//     for(int i = 0; i < length; i++) {
//         state = prefix_search(state, *(test_word+i));
//         if (!state) {
//             printf("\nnot found");
//             found = 0;
//             break;
//         }
//     }

//     if (found) printf("found");

//     return 0;
// }


