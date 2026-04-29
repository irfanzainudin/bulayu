# Finite phonotactic parser for Malay words
# Penghurai fonotaktik terbatas untuk perkataan Melayu

from phonotactics import PHONOTACTICS
from senarai_kata import senarai_kata, skip_words

MM_ONSET = PHONOTACTICS["mm"]["ONSET"]
MM_NUCLEUS = PHONOTACTICS["mm"]["NUCLEUS"]
MM_CODA = PHONOTACTICS["mm"]["CODA"]

LONGEST_ONSET_IN_MM = max(MM_ONSET, key=len)
LENGTH_OF_LONGEST_MM_ONSET = len(LONGEST_ONSET_IN_MM)

LONGEST_CODA_IN_MM = max(MM_CODA, key=len)
LENGTH_OF_LONGEST_MM_CODA = len(LONGEST_CODA_IN_MM)

class SyllableUnit():
    def __init__(self, onset="", nucleus="", coda=""):
        self.onset:str = onset
        self.nucleus:str = nucleus
        self.coda:str = coda
    
    # def append(self, item):
    #     """Adds a single item to the end of the collection."""
    #     self._data.append(item)

    def __len__(self):
        return len(self.onset) + len(self.nucleus) + len(self.coda)
    
    def __str__(self):
        return f"onset: {self.onset}, nucleus: {self.nucleus}, coda: {self.coda}"
    
    def to_string(self):
        return f"{self.onset}{self.nucleus}{self.coda}"

# Alias
SukuKata = SyllableUnit

class Word():
    def __init__(self):
        self.syllables: list[SyllableUnit] = []

# Alias
Kata = Word

def find_coda(substr_between_nuclei:str):
    # NOTE: Does this fix the IndexError?
    if len(substr_between_nuclei) == 0:
        return ""
    
    substr = substr_between_nuclei
    i = len(substr)
    while i > 0:
        if substr[:i] in MM_CODA:
            return substr[:i]
        else:
            i -= 1
    
    return substr[0]

def parse(word:str) -> SyllableUnit:
    parsed = []

    index = 0
    while index != len(word):
        # NSU == New SyllableUnit
        nsu = SyllableUnit()
        
        # Current char is a vowel
        if word[index] in MM_NUCLEUS:
            nsu.nucleus = word[index]

            # Is there coda?
            next_idx = index + 1
            next_vowel_idx = min(
                [
                    word[next_idx:].index(nc)
                    if
                        nc in word[next_idx:]
                        and
                        word[next_idx:].index(nc) > index
                    else 999
                    for nc in MM_NUCLEUS
                ]
            )
            # Adjust the index of next vowel so it's accurate
            # ... with respect to the full length of the word
            next_vowel_idx += next_idx
            coda = find_coda(word[index + 1:next_vowel_idx])
            nsu.coda = coda
        # Current char is a consonant
        else:
            # Find longest onset
            next_idx = index + 1
            next_vowel_idx = min(
                [
                    word[next_idx:].index(nc)
                    if
                        nc in word[next_idx:]
                        and
                        word[next_idx:].index(nc) > index
                    else 999
                    for nc in MM_NUCLEUS
                ]
            )
            onset_length = -999
            i = next_vowel_idx
            while i > index:
                if word[index:i] in MM_ONSET:
                    onset_length = i - index
                    nsu.onset = word[index:i]
                    break
                else:
                    i -= 1
    
            # Find nucleus
            if (index + onset_length) > 0 and (index + onset_length) < len(word):
                nsu.nucleus = word[index + onset_length]
            # else:
            #     nsu.nucleus = word[]

            # Is there coda?
            if index + onset_length == len(word):
                break
            # There is coda:
            next_idx = index + onset_length + 1
            next_vowel_idx = min(
                [
                    word[next_idx:].index(nc)
                    if
                        nc in word[next_idx:]
                        and
                        word[next_idx:].index(nc) > index
                    else 999
                    for nc in MM_NUCLEUS
                ]
            )
            # Adjust the index of next vowel so it's accurate
            # ... with respect to the full length of the word
            next_vowel_idx += next_idx
            coda = find_coda(word[next_idx:next_vowel_idx])
            nsu.coda = coda
        
        parsed.append(nsu)
        index += len(nsu)
    
    # Check for misplaced codas
    for j, su in enumerate(parsed):
        if j < len(parsed) - 1:
            next_su = parsed[j+1]
            if su.coda != "" and next_su.onset == "":
                next_su.onset = su.coda
                su.coda = ""

    return parsed

# words = [
#     "aturan",
#     "penerangan",
#     "anjing",
#     "nama saya irfan",
#     # "plastik", # TODO: incorrect parsing
#     "swasta" # TODO: breaks the parsing algorithm
#     "masyarakat"
# ]
# parsed_words = [parse(pw) for pw in words]
# for pw in parsed_words:
#     ps = ""
#     for p in pw:
#         ps += p.to_string()
#         ps += '/'
#     print(ps)

# Parsing words in senarai_kata
# parsed_sk = []
# for j, k in enumerate(senarai_kata):
#     # TODO: Need to fix this bug
#     if k in skip_words or 'z' in k:
#         parsed_sk.append(k)
#         continue
#     # print(f"{j}. Current word: {k}")
#     parsed_k = parse(k)
#     psk = []
#     for p in parsed_k:
#         psk.append(p.to_string())
#     # parsed_k = "".join([p.to_string() + '/' for p in parsed_k])
#     # parsed_sk.append(parsed_k)
#     parsed_sk.append(psk)
# with open("parsed_senarai_kata.py", "w") as psk:
#     psk.write(str(parsed_sk))
