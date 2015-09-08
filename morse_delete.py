#!/usr/bin/env python

import argparse
import glob
import os
import sys
import trie

morse_dict = {
'A' : '.-', 'a' : '.-', 'B' : '-...', 'b' : '-...', 'C' : '-.-.', 'c' : '-.-.', 'D' : '-..', 'd' : '-..',
'E' : '.', 'e' : '.', 'F' : '..-.', 'f' : '..-.', 'G' : '--.', 'g' : '--.','H' : '....', 'h' : '....',
'I' : '..', 'i' : '..', 'J' : '.---', 'j' : '.---', 'K' : '-.-', 'k' : '-.-', 'L' : '.-..', 'l' : '.-..',
'M' : '--', 'm' : '--', 'N' : '-.', 'n' : '-.', 'O' : '---', 'o' : '---', 'P' : '.--.', 'p' : '.--.',
'Q' : '--.-', 'q' : '--.-', 'R' : '.-.', 'r' : '.-.', 'S' : '...', 's' : '...', 'T' : '-', 't' : '-',
'U' : '..-', 'u' : '..-', 'V' : '...-', 'v' : '...-', 'W' : '.--', 'w' : '.--', 'X' : '-..-', 'x' : '-..-',
'Y' : '-.--', 'y' : '-.--', 'Z' : '--..', 'z' : '--..', ' ' : ''
}

letter_dict = { '.-' : 'A', '-...' : 'B', '-.-.' : 'C', '-..' : 'D', '.' : 'E', '..-.' : 'F', '--.' : 'G',
'....' : 'H', '..' : 'I', '.---' : 'J', '-.-' : 'K', '.-..' : 'L', '--' : 'M', '-.' : 'N', '---' : 'O',
'.--.' : 'P', '--.-' : 'Q', '.-.' : 'R', '...' : 'S', '-' : 'T', '..-' : 'U', '...-' : 'V', 
'.--' : 'W', '-..-' : 'X', '-.--' : 'Y', '--..' : 'Z' 
}


morse_sentences = []
letter_sentences = []
found_phrases = []
d = trie.Trie();

def print_remaining(cur_words, cache_index, word_gen_cache):

#    print "cache called with: " + "".join(cur_words) + " at " + str(cache_index)
#    print word_gen_cache

    if cache_index == 0:
        print " ".join(cur_words)
        found_phrases.append(" ".join(cur_words))
        return

    try:
        for word in word_gen_cache[cache_index]:
            cur_words.append(word)
            print_remaining(cur_words, cache_index-len(word), word_gen_cache)
            cur_words.pop()
    except KeyError:
        # no valid words on this path
        return


def rec_parse_to_words(cur_words, remaining_letters, word_gen_cache):
    # if there are no remaining letters
    if len(remaining_letters) == 0:
        print " ".join(cur_words)
        found_phrases.append(" ".join(cur_words))
        return

    # if we've already found all the remaining words at this index, iterate through and print 
    if len(remaining_letters) in word_gen_cache:
#        print "using cache"
        print_remaining(cur_words, len(remaining_letters), word_gen_cache)
        return

    # else, grab a letter, is it word?  if so
    word = ""
    for letter in remaining_letters:
        word += letter
#        print "trying: " + word + " remaining letters: " + remaining_letters
        if d.is_word(word):
#            print "found a word: " + word
            cur_words.append(word)
#            print "adding " + word + " to cache at pos " + str(len(remaining_letters))
            if len(remaining_letters)in word_gen_cache:
                word_gen_cache[len(remaining_letters)].append(word)
            else:
                word_gen_cache[len(remaining_letters)] = []
                word_gen_cache[len(remaining_letters)].append(word)

            rec_parse_to_words(cur_words, remaining_letters[len(word):], word_gen_cache)       
            cur_words.pop()


def parse_to_words(cur_sentence):
    if cur_sentence not in letter_sentences:
        letter_sentences.append(cur_sentence)
        print "Ready to parse: " + cur_sentence

        #woot, now recursively parse this into real words
        rec_parse_to_words([], cur_sentence, {})


def rec_generate_sentences(cur_words, cur_sentence, morse):
    if len(morse) == 0:
        if len(cur_sentence) == 0 or d.is_word(cur_sentence):
 #           print "all morse letters used!  victory!"
            print " ".join(cur_words)
        return

    # for each letter, have to try it until we run out of matches
    for num in range(1,4):
        try:
            letter = letter_dict[morse[0:num]]
            newword = cur_sentence + letter
 #           print "Trying " + letter + " to get " + newword  + " remaining: " + morse
 #           print cur_words
            if d.is_word(newword):
#                print "It's a valid word"
                cur_words.append(newword)
                rec_generate_sentences(cur_words, "", morse[num:])
 #               print "removing " + newword 
                cur_words.remove(newword)

            if d.is_prefix(newword):
 #               print "It's a valid prefix!"
                rec_generate_sentences(cur_words, cur_sentence+letter, morse[num:])
        except KeyError:
            # just catch and suppress this error
            print morse[0:num] + " is not a valid morse letter"
        except IndexError:
            # hitting the end of the array
            # print "not enough letters to parse, we should just bail"
            return

def generate_sentences(morse):
    # check if we've already looked at this phrase
    if morse in morse_sentences:
#        print "We've already seen: " + morse
        return

    morse_sentences.append(morse)
    print "ready to gen: " + morse
    rec_generate_sentences([], '', morse)

            
def rec_generate_morse_phrase(cur_phrase, morse_phrase, morse_letter):
    # print "cur_phrase: " + cur_phrase + " morse_phrase: " + morse_phrase + " letter: " + morse_letter
    # if we have no more letters to delete, call new function to parse for words
    if len(morse_letter) == 0:
        generate_sentences(cur_phrase + morse_phrase)
        return

    # if we've run out of morse letters to consider deleting, return
    if len(morse_phrase) == 0:
        return

    # try it without the delete
    rec_generate_morse_phrase(cur_phrase + morse_phrase[0], morse_phrase[1:], morse_letter)

    # if the next character is eligible to be deleted, try with the delete
    if morse_phrase[0] == morse_letter[0]:
        rec_generate_morse_phrase(cur_phrase, morse_phrase[1:],morse_letter[1:])
        

def generate_morse_phrases(morse_phrase, morse_letter):
    rec_generate_morse_phrase('', morse_phrase, morse_letter)

def load_dictionary():
    f = open("sowpods.txt", 'r')
    print "loading up SOWPODS..."
    for line in f:
        d.insert(line.strip())
    print "SOWPODS loaded!"

    print "IS BAT a prefix? (should be True)"
    print d.is_prefix("BAT")
    print "is ZULA a prefix? (should be False)"
    print d.is_prefix("ZULA")
    print "is BA a prefix? (should be True)"
    print d.is_prefix("BA")
    print "is BATMAN a word? (should be True)"
    print d.is_word("BATMAN")
    print "is BAT a word? (should be True)"
    print d.is_word("BAT")

def main(argv=None):
    # handle options
    parser = argparse.ArgumentParser(description='Find valid english phrases when a morse letter is removed')
    parser.add_argument('-p', '--phrase', help='Original phrase')
    parser.add_argument('-l', '--letter',
                        help='Letter to remove')

    args = parser.parse_args()

    phrase = args.phrase;
    letter = args.letter;

    print "removing " + letter + " from " + phrase
    print "Translating " + phrase + " into morse..." 

    morse_phrase = ""
    for c in phrase:
        morse_phrase += morse_dict[c]

    print morse_phrase
    morse_letter = morse_dict[letter]

    load_dictionary()
    generate_morse_phrases(morse_phrase, morse_letter)

    print found_phrases

if __name__ == "__main__":
    sys.exit(main())
