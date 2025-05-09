import time
import enlighten
from penghurai import hurai
from senarai_kata import senarai_kata, pembahagian_suku_kata_untuk_senarai_kata as psk

jumlah_kata = len(senarai_kata)

manager = enlighten.get_manager()
progress_bar = manager.counter(total=jumlah_kata, desc='Testing', unit='ticks')

for i, kata in enumerate(senarai_kata):
    if hurai(kata) != psk[i]:
        print("WRONG")
    time.sleep(0.01)
    progress_bar.update()