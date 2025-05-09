# Penghurai = Parser
from senarai_kata import senarai_kata

suku_kata_melayu = [
    'a', 'ba', 'ca', 'da', 'ea', 'fa',
    'ga', 'ha', 'ia', 'ja', 'ka', 'la',
    'ma', 'na', 'oa', 'pa', 'qa', 'ra',
    'sa', 'ta', 'ua', 'va', 'wa', 'xa',
    'ya', 'za',
    # E / e = e pepet
    'ae', 'be', 'ce', 'de', 'ee', 'fe',
    'ge', 'he', 'ie', 'je', 'ke', 'le',
    'me', 'ne', 'oe', 'pe', 'qe', 're',
    'se', 'te', 'ue', 've', 'we', 'xe',
    'ye', 'ze',
    # É / é = e taling
    'aé', 'bé', 'cé', 'dé', 'eé', 'fé',
    'gé', 'hé', 'ié', 'jé', 'ké', 'lé',
    'mé', 'né', 'oé', 'pé', 'qé', 'ré',
    'sé', 'té', 'ué', 'vé', 'wé', 'xé',
    'yé', 'zé',
    'ai', 'bi', 'ci', 'di', 'ei', 'fi',
    'gi', 'hi', 'ii', 'ji', 'ki', 'li',
    'mi', 'ni', 'oi', 'pi', 'qi', 'ri',
    'si', 'ti', 'ui', 'vi', 'wi', 'xi',
    'yi', 'zi',
    'ao', 'bo', 'co', 'do', 'eo', 'fo',
    'go', 'ho', 'io', 'jo', 'ko', 'lo',
    'mo', 'no', 'oo', 'po', 'qo', 'ro',
    'so', 'to', 'uo', 'vo', 'wo', 'xo',
    'yo', 'zo',
    'au', 'bu', 'cu', 'du', 'eu', 'fu',
    'gu', 'hu', 'iu', 'ju', 'ku', 'lu',
    'mu', 'nu', 'ou', 'pu', 'qu', 'ru',
    'su', 'tu', 'uu', 'vu', 'wu', 'xu',
    'yu', 'zu',
]

onsets = [
    # Single-letter onsets
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
    'i',' j', 'k', 'l', 'm', 'n', 'o', 'p',
    'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
    'y', 'z',
    # Double-letter onsets
    'kh', 'ng', 'sh', 'sy',
]

nuclei = [
    'a', 'e', 'é', 'i', 'o', 'u'
]

coda = [
    # Single-letter
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
    'i',' j', 'k', 'l', 'm', 'n', 'o', 'p',
    'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
    'y', 'z',
    # Double-letter
    'kh', 'ng', 'sh', 'sy',
]

unit_dua_huruf = [
    'kh', 'ng', 'sh', 'sy',
]

huruf_pertama_dalam_unit_dua_huruf = [
    'k', 'n', 's'
]

huruf_kedua_dalam_unit_dua_huruf = [
    'h', 'n', 's'
]

def penentuan_onset(kata) -> dict:
    pembahagian = {}

    for i, huruf in enumerate(kata):
        if huruf == 'k':
            pembahagian['onset'] = huruf
            if kata[i + 1] == 'h':
                pembahagian['onset'] = kata[i : i + 2]
        elif huruf == 'n':
            pembahagian['onset'] = huruf
            if kata[i + 1] == 'g':
                pembahagian['onset'] = kata[i : i + 2]
        elif huruf == 's':
            pembahagian['onset'] = huruf
            if kata[i + 1] == 'h' or kata[i + 1] == 'y':
                pembahagian['onset'] = kata[i : i + 2]
        # if kata[:2] in unit_dua_huruf:
        #     pembahagian['onset'] = kata[:2]
    
    return pembahagian

def penentuan_nukleus(kata) -> dict:
    pembahagian = {}

    for i, huruf in enumerate(kata):
        if huruf == 'k':
            pembahagian['onset'] = huruf
            if kata[i + 1] == 'h':
                pembahagian['onset'] = kata[i : i + 2]
        elif huruf == 'n':
            pembahagian['onset'] = huruf
            if kata[i + 1] == 'g':
                pembahagian['onset'] = kata[i : i + 2]
        elif huruf == 's':
            pembahagian['onset'] = huruf
            if kata[i + 1] == 'h' or kata[i + 1] == 'y':
                pembahagian['onset'] = kata[i : i + 2]
    
    return pembahagian

def segmen(kata):
    onset = penentuan_onset(kata)
    nukleus = penentuan_nukleus(kata)

    return [onset]

def pembahagian_suku_kata(kata):
    pembahagian = []
    huruf_yang_boleh_bersambung_dengan_a = [
        'n',
        'm',
    ]

    for i, huruf in enumerate(kata):
        jep = len(pembahagian) # jep == Jumlah elemen dalam `pembahagian`
        if huruf == 'a':
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
            if jep > 0:
                pembahagian[jep - 1] += huruf
            else:
                pembahagian.append(huruf)
        elif huruf == 'f':
            pembahagian.append(huruf)
        elif huruf == 'g':
            elemen_sebelum = pembahagian[jep - 1]
            panjang_elemen_sebelum = len(elemen_sebelum)
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

def hurai(kata):
    # segmentasi = segmen(kata)

    # return segmentasi
    pembahagian = pembahagian_suku_kata(kata)

    return pembahagian


def main():
    # print(segmen(input("Minta kata: ")))
    while True:
        kata = input(">> ")
        
        if kata == 'q' or kata == 'e' or kata == 'quit' or kata == 'exit':
            break
        else:
            print(hurai(kata))

if __name__ == "__main__":
    main()
