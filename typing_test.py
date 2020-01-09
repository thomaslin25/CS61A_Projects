""" Typing Test implementation """

from utils import *
from ucb import main

# BEGIN Q1-5
def lines_from_file(path):
    file = open(path)
    paragraph = []
    if readable(file):
        for lines in readlines(file):
            line = strip(lines)
            paragraph.append(line)
    close(file)    
    return paragraph
def new_sample(path, i):
    paragraph = lines_from_file(path)
    return paragraph[i]
def analyze(sample_paragraph, typed_string, start_time, end_time):
    def wpm(sample_paragraph, start_time, end_time):
        num_characters = len(typed_string)
        num_words = num_characters/5
        seconds = end_time - start_time
        return (num_words * 60)/seconds
    def accuracy(sample_paragraph, typed_string):
        words_sample = split(sample_paragraph)
        user_sample = split(typed_string)
        words_right, total_words = 0,0
        if len(user_sample) == 0 or len(words_sample) == 0:
            return 0.0
        while range(len(user_sample)) and range(len(words_sample)):
            sample_word, user_word = words_sample[0], user_sample[0]
            if sample_word == user_word:
                words_right += 1
            total_words += 1
            user_sample, words_sample = user_sample[1:], words_sample[1:]
        return words_right * 100 / total_words
    return [wpm(sample_paragraph, start_time, end_time), accuracy(sample_paragraph, typed_string)]
def pig_latin(string):
    def is_vowel(s):
        if s == "a" or s == "e" or s == "i" or s == "o" or s == "u":
            return True
        return False
    if is_vowel(string[0]):
        return string + 'way'
    removed = ''
    while len(string) > 0:
        if is_vowel(string[0]):
            return string + removed + 'ay'
        removed += string[0]
        string = string[1:]
    return removed + 'ay'
# END Q1-5
def autocorrect(usr_input, words_list, score_function):
    comparison = []
    for word in words_list:
        if usr_input == word:
            return word
    return min(words_list, key=lambda words_list: score_function(usr_input, words_list))
def swap_score(usr, word):
    if usr == '' or word =='':
        return 0
    if usr[0] != word[0]:
        return 1 + swap_score(usr[1:], word[1:])
    else:
        return swap_score(usr[1:], word[1:])
# Question 6

def score_function(word1, word2):
    """A score_function that computes the edit distance between word1 and word2."""

    if word1 == '' and word2 == '': # Fill in the condition
        # BEGIN Q6
        return 0
        # END Q6
    elif word2 == '':
        return 1 + score_function(word1[1:], word2)
    elif word1 == '':
        return len(word2)
    elif word1[0] == word2[0]: # Feel free to remove or add additional cases
        # BEGIN Q6
        return score_function(word1[1:], word2[1:])
        # END Q6

    else:
        add_char = 1 + score_function(word2[0] + word1, word2[0:])  # Fill in these lines
        remove_char = 1 + score_function(word1[1:], word2[0:]) 
        substitute_char = 1 + score_function(word2[0] + word1[1:], word2[0:])
        # BEGIN Q6
        return min(add_char, remove_char, substitute_char)
        # END Q6

KEY_DISTANCES = get_key_distances()

# BEGIN Q7-8
def score_function_accurate(word1, word2):
    if word1 == '' and word2 == '':
        return 0
    elif word2 == '':
        return len(word1)
    elif word1 == '':
        return len(word2)
    elif word1[0] == word2[0]:
        return score_function_accurate(word1[1:], word2[1:])
    else: 
        add_char = 1 + score_function_accurate(word2[0] + word1, word2[0:])  # Fill in these lines
        remove_char = 1 + score_function_accurate(word1[1:], word2[0:]) 
        substitute_char = (KEY_DISTANCES[word1[0], word2[0]] + (score_function_accurate(word2[0] + word1[1:], word2[0:])))
        return min(add_char, remove_char, substitute_char)
memo = {}
def score_function_final(word1, word2):
    x = word1 + '_' + word2
    y = word2 + '_' + word1
    if x in memo:
        return memo[x]
    if y in memo:
        return memo[y]
    if word1 == '' and word2 == '':
        return 0
    elif word2 == '':
        return len(word1)
    elif word1 == '':
        return len(word2)
    elif word1[0] == word2[0]:
        yes = score_function_final(word1[1:], word2[1:])
        memo[x] = yes
        memo[y] = yes
        return memo[x]
    else: 
        add_char = 1 + score_function_final(word2[0] + word1, word2[0:])  # Fill in these lines
        remove_char = 1 + score_function_final(word1[1:], word2[0:]) 
        substitute_char = (KEY_DISTANCES[word1[0], word2[0]] + (score_function_final(word2[0] + word1[1:], word2[0:])))
        score = min(add_char, remove_char, substitute_char)
        memo[x] = score
        memo[y] = score
        return memo[x]


    x = word1 + '_' + word2
    y = word2 + '_' + word1
    if x not in memo or y not in memo:
        value = score_function_accurate(word1, word2)
        memo[x] = value
        memo[y] = value
    return memo[x]
# END Q7-8

