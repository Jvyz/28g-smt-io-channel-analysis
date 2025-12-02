import skrf as rf
import matplotlib.pyplot as plt
import numpy as np

files = {
    "4-inch": "TEC_SMT_IO_42GHz_Thru_B5B6_4in.s4p",
    "10-inch": "TEC_SMT_IO_42GHz_Thru_B5B6_10in.s4p"
}

plt.figure(figsize=(12, 7))

for label, f in files.items():
    try:
        net = rf.Network(f)
    except Exception as e:
        print(f"Error Loading {f}: {e}")
        continue
    
    mag_s21 = np.abs(net.s[0, 1, 0])
    mag_s31 = np.abs(net.s[0, 2, 0])
    mag_s41 = np.abs(net.s[0, 3, 0])

    print(f"{f} s21: = {mag_s21}")
    print(f"{f} s31: = {mag_s31}")
    print(f"{f} s41: = {mag_s41}")