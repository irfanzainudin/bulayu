import re
from parser import parse, SyllableUnit

# vowels in Malay
VOWELS = "aeiou"

def syllabify(word):
    word = word.lower()
    syllables = []
    current = ""
    
    i = 0
    while i < len(word):
        current += word[i]
        
        # if current char is a vowel
        if word[i] in VOWELS:
            # lookahead: diphthongs
            if i + 1 < len(word) and word[i:i+2] in ["ai", "au", "oi"]:
                current += word[i+1]
                i += 1
            
            # end syllable if next is consonant-vowel
            if i + 1 < len(word):
                if word[i+1] not in VOWELS:
                    # lookahead further: consonant + vowel
                    if i + 2 < len(word) and word[i+2] in VOWELS:
                        syllables.append(current)
                        current = ""
            else:
                # end of word
                syllables.append(current)
                current = ""
        
        i += 1
    
    if current:
        syllables.append(current)
    
    return syllables

def show_parsed(parsed: list[SyllableUnit]):
    return [p.to_string() for p in parsed]

# test
words = ["makan", "pantun", "kerbau", "sayang", "bunga", "sungguh", "pandai", "dunia"]
for w in words:
    print(w, "→", syllabify(w), "vs", show_parsed(parse(w)))
