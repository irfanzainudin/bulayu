import time
import enlighten
from penghurai import hurai
from senarai_kata import senarai_kata, pembahagian_suku_kata_untuk_senarai_kata as psk

# You may need to change color settings
class Colours: 
    RED = '\033[31m'
    ENDC = '\033[m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'

JUMLAH_KATA = len(senarai_kata)

manager = enlighten.get_manager()
progress_bar = manager.counter(total=JUMLAH_KATA, desc='Testing', unit='tests')

failed = 0
passed = 0
for i, kata in enumerate(senarai_kata):
    if hurai(kata) != psk[i]:
        # print(Colours.RED + "FAILED" + Colours.ENDC)
        failed += 1
    else:
        # print(Colours.GREEN + "PASSED" + Colours.ENDC)
        passed += 1
    # To slow down time and appreciate the beauty
    # that is the art of testing your software
    time.sleep(0.001)
    progress_bar.update()

print(Colours.RED + f"FAILED: {failed}" + Colours.ENDC)
print(Colours.GREEN + f"PASSED: {passed}" + Colours.ENDC)

print(Colours.BLUE + "\n======================\nCORRECTNESS PERCENTAGE: " + f"{((passed / JUMLAH_KATA) * 100):.2f}%" + "\n======================" + Colours.ENDC)