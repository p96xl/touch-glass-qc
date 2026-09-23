# Live pressure readout: wiper (A2) on internal pullup, all 4 corners grounded.
# Harder press -> lower resistance. Ohms are approximate: the Nano's pullup is 20-50k, assumed 35k.
import math, statistics, time
from host import q
RPU = 35000  # knob: measure with a known resistor once parts arrive
end, got = time.time() + 25, []
print('press the glass: light, then medium, then hard (25 s)')
while time.time() < end:
    v = q('LLULL')[2]
    if v >= 1015: print('   not touched'); time.sleep(.1); continue
    r = RPU * v / (1023 - v)
    got.append(r)
    # log bar: 1k = full (hard press), 100k = empty (barely touching)
    print(f'{r:9.0f} ohm  ' + '#' * max(1, min(40, int(40 * (1 - math.log10(max(r, 1000) / 1000) / 2)))))
    time.sleep(.1)
if got: print(f'hardest {min(got):.0f} ohm   typical {statistics.median(got):.0f} ohm   light-contact samples (>3k) {sum(r > 3000 for r in got)}/{len(got)}')
else: print('never registered a touch')
