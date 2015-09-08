#!/usr/bin/env python
# taken randomly off the internet and then gutted
__name__ = "trie"

class Node:
    """Node for Python Trie Implementation"""
    
    def __init__(self):
        self.validWord = False
        self.nodes = {} # dict of subsequent letters
        
    def __print_all__(self):
        """Get all of the words in the trie"""
        print self.nodes
        for key in self.nodes:
            print key + " " + str(self.nodes[key].validWord)
            self.nodes[key].__print_all__()
        
 
    def __str__(self):
        return self.word
    
    def __insert__(self, word):
        """Add a word to the node in a Trie"""
        current_letter = word[0]
        
        # Create the Node if it does not already exist
        if current_letter not in self.nodes:
            self.nodes[current_letter] = Node()

        if len(word) == 1:
            self.nodes[current_letter].validWord = True
        else:
            # keep going doing the chain
            self.nodes[current_letter].__insert__(word[1:])


    def __is_word__(self, word):
        # if is in our wordset, keep looking
        if word[0] in self.nodes:
            if len(word) == 1:
                return self.nodes[word[0]].validWord
            else:
                return self.nodes[word[0]].__is_word__(word[1:])
        else:
            return False

    def __is_prefix__(self, word):
        if word[0] in self.nodes:
            if len(word) == 1:
                return True
            else:
                return self.nodes[word[0]].__is_prefix__(word[1:])
        else:
            return False


class Trie:
   """Trie Python Implementation"""
  
   def __init__(self):
        self.root = Node()
        
   def insert(self, word):
        self.root.__insert__(word.lower())
        
   def is_prefix(self, prefix):
       return self.root.__is_prefix__(prefix.lower())

   def is_word(self, word):
       return self.root.__is_word__(word.lower())

   def print_all(self):
        return self.root.__print_all__()



