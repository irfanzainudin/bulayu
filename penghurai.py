# Penghurai = Parser

import tomllib as tl
from itertools import combinations, permutations
from senarai_kata import senarai_kata
from pemalar import VOKAL as VOWELS, KONSONAN as CONSONANTS, SYLLABLE_RULES
from parser import parse
from util import print_help

# Load Tatabunyi from TOML file
with open('Tatabunyi.toml', 'rb') as ttt:
    TT = tl.load(ttt)

CONSTRUCTED_SYLLABLE_RULES = []

# Indeks dalam Tatabunyi.toml
MELAYU_LAMA = 0
MELAYU_KLASIK = 1
MELAYU_MODEN = 2
LIS_ONSET: list = TT['phonotactic'][MELAYU_MODEN]['definition']['onset'][0]
LIS_MULTIGRAF_ONSET = list(set([x for x in LIS_ONSET if len(x) > 1]))
LIS_HURUF_PERTAMA_MULTIGRAF_ONSET = list(set([x[0] for x in LIS_MULTIGRAF_ONSET if True]))
LIS_NUCLEUS = TT['phonotactic'][MELAYU_MODEN]['definition']['nucleus'][0]
LIS_CODA = TT['phonotactic'][MELAYU_MODEN]['definition']['coda'][0]
LIS_MULTIGRAF_CODA = list(set([x for x in LIS_CODA if len(x) > 1]))
LIS_HURUF_PERTAMA_MULTIGRAF_CODA = list(set([x[0] for x in LIS_MULTIGRAF_CODA if True]))
# print(LIS_HURUF_PERTAMA_MULTIGRAF_ONSET)
# print(LIS_HURUF_PERTAMA_MULTIGRAF_CODA)

# Normalised form = 1's and 0's
# Where 1's are consonants
# And   0's are vowels
def convert_to_normalised_form(kata):
    nf = ""

    for huruf in kata:
        if huruf in CONSONANTS:
            nf += '1'
        else: # huruf in VOWELS
            nf += '0'
    
    return nf

# SF = Syllabified Form
def convert_to_syllabified_form(kata, most_probable_syllable_rule):
    mpsr = most_probable_syllable_rule
    syllable = ""
    sf = []
    
    i = -1
    j = 0
    for char in mpsr:
        i += 1
        if char == '-':
            sf.append(syllable)
            syllable = ""
        else:
            syllable += kata[j]
            j += 1
        
        # To append before exiting loop
        if i == (len(mpsr) - 1):
            sf.append(syllable)

    return sf

def generate_possible_permutations_of_malay_syllable_structure():
    possible_permutations = {}
    
    combos = [
        'V',
        'VC', 'CV',
        'VCC', 'CVC', 'CCV',
        'CVCC', 'CCVC', 'CCCV', # 'VCCC',
        'CCCVC'
    ]
    combos = [
        '0',
        '01', '10',
        '011', '101', '110',
        '1011', '1101', '1110', # 'VCCC',
        '11101'
    ]
    
    # NOTE: Thirteen because the longest syllable structure
    # in Malay is twelve according to this research paper:
    # https://www.wseas.us/e-library/conferences/2011/Venice/ACACOS/ACACOS-47.pdf
    for num_of_syllable_structures in range(1, 13):
        for combo in permutations(combos, num_of_syllable_structures):
        # for combo in combinations(combos, num_of_syllable_structures):
            # print(''.join(str(i) for i in combo))
            joined_combo = ''.join(str(i) for i in combo)
            possible_permutations[joined_combo] = joined_combo

    # NOTE: 4337114 possible permutations. Hence, 4337114 syllable rules
    # print(len(possible_permutations))
    
    return possible_permutations

def generate_possible_combinations_of_malay_syllable_structure():
    possible_combinations = {}
    
    combos = [
        'V',
        'VC', 'CV',
        'VCC', 'CVC', 'CCV',
        'CVCC', 'CCVC', 'CCCV', # 'VCCC',
        'CCCVC'
    ]
    combos = [
        '0',
        '01', '10',
        '011', '101', '110',
        '1011', '1101', '1110', # 'VCCC',
        '11101'
    ]
    
    # NOTE: Thirteen because the longest syllable structure
    # in Malay is twelve according to this research paper:
    # https://www.wseas.us/e-library/conferences/2011/Venice/ACACOS/ACACOS-47.pdf
    for num_of_syllable_structures in range(1, 13):
        for combo in combinations(combos, num_of_syllable_structures):
            # print(''.join(str(i) for i in combo))
            joined_combo = ''.join(str(i) for i in combo)
            possible_combinations[joined_combo] = joined_combo

    # NOTE: 928 possible combinations. Hence, 928 syllable rules
    # print(len(possible_combinations))
    
    return possible_combinations

# Based on this research paper:
# https://www.wseas.us/e-library/conferences/2011/Venice/ACACOS/ACACOS-47.pdf
def syllabification_using_rules_matching(kata) -> list:
    segmentation = []
    
    nf = convert_to_normalised_form(kata)

    if nf in SYLLABLE_RULES.keys():
        most_probable_syllable_rule = SYLLABLE_RULES[nf]
    else:
        most_probable_syllable_rule = nf
    
    # SF = Syllabified Form
    sf = convert_to_syllabified_form(kata, most_probable_syllable_rule)
    print(sf)

    possible_combinations = generate_possible_combinations_of_malay_syllable_structure()
    
    # Save the possible combinations in a file
    with open('pcpsr.py', 'w') as pcpsr:
        pcpsr.write(str(possible_combinations))

    # possible_permutations = generate_possible_permutations_of_malay_syllable_structure()
    
    # with open('pppsr.py', 'a') as pppsr:
    #     pppsr.write('{\n')
    #     for key, value in possible_permutations.items():
    #         pppsr.write(f"\"{key}\": \"{value}\",\n")
    #     pppsr.write('}\n')
    
    segmentation = nf
    return segmentation

def segmen(kata) -> list:
    lis_segmentasi = []
    segmentasi = {}
    jumpa_nucleus = False
    segmen_kini = ""
    
    indeks_mula_suku_kata = 0
    len_kata = len(kata)
    for i, huruf in enumerate(kata):
        if huruf in LIS_NUCLEUS:
            # Set onset
            if kata[indeks_mula_suku_kata : i] != '':
                segmentasi['onset'] = kata[indeks_mula_suku_kata : i]
            
            # Set nucleus
            segmentasi['nucleus'] = huruf
            
            # Set coda
            if (i < len_kata - 1) and kata[i + 1] in LIS_CODA:
                if (i < len_kata - 2):
                    if (kata[i + 1] + kata[i + 2]) in LIS_CODA:
                        segmentasi['coda'] = kata[(i + 1) : (i + 3)]
                    # else:
                    #     segmentasi['coda'] = kata[i + 1]
                else:
                    segmentasi['coda'] = kata[i + 1]
            # Update state
            indeks_mula_suku_kata = i + 1
            lis_segmentasi.append(segmentasi)
            segmentasi = {}
        else:
            continue
        # segmen_kini += huruf
        # TODO: A naïve solution at best. Needs optimisation.
        # if huruf in LIS_ONSET and jumpa_nucleus == False:
        #     if huruf in LIS_HURUF_PERTAMA_MULTIGRAF_ONSET:
        #         onset = ""
        #         for h in kata:
        #             if h in LIS_NUCLEUS:
        #                 break
        #             else:
        #                 onset += h
        #         print(onset)
        #         segmentasi['onset'] = onset
        #     elif huruf in segmentasi['onset']:
        #         continue
        #     else:
        #         segmentasi['onset'] = huruf
        
        # # NOTE: Nucleus has only single-letter units, so
        # # no need to check for digraphs or trigraphs
        # if huruf in LIS_NUCLEUS:
        #     segmentasi['nucleus'] = huruf
        #     jumpa_nucleus = True
        
        # # TODO: A naïve solution at best. Needs optimisation.
        # if huruf in LIS_CODA and jumpa_nucleus == True:
        #     if (i < len_kata - 1) and ((huruf + kata[i + 1]) in LIS_CODA):
        #         # NOTE: Because the max length of a coda
        #         # is two in the Malay coda set, we just
        #         # need to check if it's less than the
        #         # length of `kata` minus one. If in the
        #         # future, we accepted a trigraph in the
        #         # Malay coda set, then this code needs
        #         # to change.
        #         if i < len_kata - 1:
        #             segmentasi['coda'] = huruf + kata[i + 1]
        #     else:
        #         segmentasi['coda'] = huruf
        #     # segmentasi['coda'] = huruf
            
        #     # Reset to form a new syllable
        #     lis_segmentasi.append(segmentasi)
        #     segmen_kini = ""
        #     segmentasi = {}
        #     jumpa_nucleus = False

    return lis_segmentasi

def pembahagian_suku_kata(kata):
    pembahagian = []
    huruf_yang_boleh_bersambung_dengan_a = [
        'n',
        'm',
    ]

    for i, huruf in enumerate(kata):
        jep = len(pembahagian) # jep == Jumlah elemen dalam `pembahagian`
        # elemen_sebelum = pembahagian[jep - 1] if jep > 0 else ""
        # panjang_elemen_sebelum = len(elemen_sebelum)
        
        # Untuk 
        # To capture the first letter
        if jep <= 0:
            pembahagian.append(huruf)
        elif huruf == 'a':
            # TODO: This condition is already guaranteed to be
            # true by the first `if` statement, we need to find
            # another condition to check for if the letter 'a'
            # can be appended to the previous element in `pembahagian`
            if jep > 0:
                pembahagian[jep - 1] += huruf
            else:
                pembahagian.append(huruf)
        elif huruf == 'b':
            pembahagian.append(huruf)
        elif huruf == 'c':
            pembahagian.append(huruf)
        elif huruf == 'd':
            pembahagian.append(huruf)
        elif huruf == 'e':
            # TODO: This condition is already guaranteed to be
            # true by the first `if` statement, we need to find
            # another condition to check for if the letter 'a'
            # can be appended to the previous element in `pembahagian`
            if jep > 0:
                pembahagian[jep - 1] += huruf
            else:
                pembahagian.append(huruf)
        elif huruf == 'f':
            pembahagian.append(huruf)
        elif huruf == 'g':
            if i >= 0 and kata[i - 1] == 'n':
                if i >= 0 and kata[i - 2] == 'a':
                    pembahagian[jep - 1] += huruf
                else:
                    pembahagian[jep - 1] = 'ng'
            else:
                pembahagian.append(huruf)
        elif huruf == 'h':
            if i >= 0 and kata[i - 1] == 'k':
                pembahagian[jep - 1] = 'kh'
            elif i >= 0 and kata[i - 1] == 's':
                pembahagian[jep - 1] = 'sh'
            elif jep > 0 and kata[i - 1] == 'a':
                pembahagian[jep - 1] += huruf
            else:
                pembahagian.append(huruf)
        elif huruf == 'i':
            # TODO: This condition is already guaranteed to be
            # true by the first `if` statement, we need to find
            # another condition to check for if the letter 'a'
            # can be appended to the previous element in `pembahagian`
            if jep > 0:
                pembahagian[jep - 1] += huruf
            else:
                pembahagian.append(huruf)
        elif huruf == 'j':
            pembahagian.append(huruf)
        elif huruf == 'k':
            if jep > 0 and kata[i - 1] == 'u':
                pembahagian[jep - 1] += huruf
            else:
                pembahagian.append(huruf)
        elif huruf == 'l':
            pembahagian.append(huruf)
        elif huruf == 'm':
            if jep > 0 and kata[i - 1] == 'a':
                pembahagian[jep - 1] += huruf
            else:
                pembahagian.append(huruf)
        elif huruf == 'n':
            if jep > 0 and kata[i - 1] == 'a':
                pembahagian[jep - 1] += huruf
            else:
                pembahagian.append(huruf)
        elif huruf == 'o':
            # TODO: This condition is already guaranteed to be
            # true by the first `if` statement, we need to find
            # another condition to check for if the letter 'a'
            # can be appended to the previous element in `pembahagian`
            if jep > 0:
                pembahagian[jep - 1] += huruf
            else:
                pembahagian.append(huruf)
        elif huruf == 'p':
            pembahagian.append(huruf)
        elif huruf == 'q':
            pembahagian.append(huruf)
        elif huruf == 'r':
            # TODO: Tak tepat.
            # Contoh penyangkal:
            # 'angkara'
            # 'syarifah'
            if jep > 0 and kata[i - 1] == 'a':
                pembahagian[jep - 1] += huruf
            else:
                pembahagian.append(huruf)
        elif huruf == 's':
            pembahagian.append(huruf)
        elif huruf == 't':
            pembahagian.append(huruf)
        elif huruf == 'u':
            # TODO: This condition is already guaranteed to be
            # true by the first `if` statement, we need to find
            # another condition to check for if the letter 'a'
            # can be appended to the previous element in `pembahagian`
            if jep > 0:
                pembahagian[jep - 1] += huruf
            else:
                pembahagian.append(huruf)
        elif huruf == 'v':
            pembahagian.append(huruf)
        elif huruf == 'w':
            pembahagian.append(huruf)
        elif huruf == 'x':
            pembahagian.append(huruf)
        elif huruf == 'y':
            if i >= 0 and kata[i - 1] == 's':
                pembahagian[jep - 1] = 'sy'
            else:
                pembahagian.append(huruf)
        else: # huruf == 'z'
            pembahagian.append(huruf)
    
    return pembahagian

# Parse and save to file
def hurai_dan_simpan_ke_fail():
    lis_psk = []
    for i, kata in enumerate(senarai_kata):
        print(f"Elemen nombor {i}: {kata}")
        psk = pembahagian_suku_kata(kata)
        # print(psk)
        # return 0
        lis_psk.append(psk)
    
    with open('psk.py', 'w') as wpsk:
        wpsk.write(f"psk = {str(lis_psk)}")

def hurai(kata):
    pembahagian = pembahagian_suku_kata(kata)

    return pembahagian


import sys
def main():
    # print(segmen(input("Minta kata: ")))
    while True:
        kata = input(">> ")
        
        if kata == 'q' or kata == 'e' or kata == 'quit' or kata == 'exit':
            break
        # elif kata == 'save':
        #     hurai_dan_simpan_ke_fail()
        elif 's ' in kata or 'segmen ' in kata:
            katas = kata.split(' ')
            k1 = katas[1]
            segmentasi = segmen(k1)
            print(segmentasi)
            # word = ""
            # for d in segmentasi:
            #     for k, v in d.items():
            #         word += v
            # print(word)
        elif len(sys.argv) > 1 and sys.argv[1] == 'nf':
            # TODO: dodgy
            print(syllabification_using_rules_matching(kata))
        elif 'h ' in kata or 'hurai ' in kata:
            # TODO: still a bit dodgy
            # e.g.
            # - penerangan
            print(hurai(kata))
        elif "h" in kata:
            print_help()
        else:
            # TODO: still a bit dodgy
            # e.g.
            # - plastik
            # - swasta
            parsed = parse(kata)
            print([p.to_string() for p in parsed])

if __name__ == "__main__":
    main()
