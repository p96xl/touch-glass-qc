import serial, sys, time
s = serial.Serial('/dev/ttyUSB0', 115200, timeout=1); time.sleep(2.2); s.reset_input_buffer()
def q(cfg):
    s.write((cfg + '\n').encode()); return [int(v) for v in s.readline().split()]
if __name__ == '__main__':
    print('pullup pin i, ground pin j -> reading at i (1023=open, low=connected)')
    print('      ' + ''.join(f'  gnd A{j}' for j in range(5)))
    for i in range(5):
        row = []
        for j in range(5):
            if i == j: row.append('    -  '); continue
            cfg = ['Z'] * 5; cfg[i] = 'U'; cfg[j] = 'L'
            row.append(f'{q("".join(cfg))[i]:7d}')
        print(f'up A{i} ' + ' '.join(row))
