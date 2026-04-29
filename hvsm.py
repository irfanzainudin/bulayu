# H vs M = Hand-written syllabification vs Machine-generated syllabification

from senarai_kata import pembahagian_suku_kata_untuk_senarai_kata as hpsk, psk as mpsk
from malaya_parsed import malaya_parsed as ampsk

def pitt(humanw, machineg):
    print(f"H_Length == M_Length => {len(humanw) == len(machineg)}")
    print(f"{len(humanw)} == {len(machineg)}")

    verdicts = []
    for i in range(len(humanw)):
        # print(humanw[i])
        # print(machineg[i])
        verdicts.append(humanw[i] == machineg[i])

    with open("vf.py", "w") as vf:
        vf.write(str(verdicts))

    mismatches = []
    for j, v in enumerate(verdicts):
        if v is False:
            # print(humanw[j], machineg[j])
            # break
            mismatches.append((humanw[j], machineg[j]))

    print(f"No. of mismatches: {len(mismatches)}")
    with open("vf.py", "a") as vf:
        vf.write('\n\n\n\n\n')
        vf.write(str(mismatches))

# pitt(hpsk, mpsk)
pitt(hpsk, ampsk)
