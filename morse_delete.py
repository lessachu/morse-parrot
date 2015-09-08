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

shitty_allowed = { 'THE', 'OF', 'FOR', 'US', 'A', 'IS', 'IT' }

shitty_min = 5
morse_sentences = []
letter_sentences = []
found_phrases = []
d = trie.Trie();

def should_filter(cur_words, shitty_count):
    return len(cur_words) > 4 or shitty_count > 2

def shitty_score(word):
    if word in shitty_allowed:
        return 0
    if len(word) < shitty_min:
        return 1
    return 0

def rec_generate_sentences(cur_words, cur_sentence, morse, shitty_count):
    if len(morse) == 0:
        cur_sentence_len = len(cur_sentence)
        if cur_sentence_len == 0 or d.is_word(cur_sentence):
            if cur_sentence_len != 0:
                cur_words.append(cur_sentence)

            if not(should_filter(cur_words, shitty_count)):
                newphrase = " ".join(cur_words)
                if not(newphrase in found_phrases):
                    print " ".join(cur_words)
                    found_phrases.append(newphrase)

            if cur_sentence_len != 0:
                cur_words.remove(cur_sentence)
        return

    # for each letter, have to try it until we run out of matches
    for num in range(1,4):
        try:
            letter = letter_dict[morse[0:num]]
            newword = cur_sentence + letter
            if d.is_word(newword):
                shitty_count += shitty_score(newword)

                if should_filter(cur_words, shitty_count):
                    # bail this sentence is too crappy
                    return

                cur_words.append(newword)
                rec_generate_sentences(cur_words, "", morse[num:], shitty_count)
                cur_words.remove(newword)

                shitty_count -= shitty_score(newword)

            if d.is_prefix(newword):
                rec_generate_sentences(cur_words, cur_sentence+letter, morse[num:], shitty_count)
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
    rec_generate_sentences([], '', morse, 0)

            
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
