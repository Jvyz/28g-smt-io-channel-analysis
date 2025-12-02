import skrf as rf
import matplotlib.pyplot as plt
from skrf import Network
import numpy as np

files = [
    "TEC_SMT_IO_42GHz_Thru_B5B6_4in.s4p",
    "TEC_SMT_IO_42GHz_Thru_B5B6_10in.s4p"
]

plt.figure(figsize=(10, 6))

for f in files:
    try:

        net = Network(f)
        net.se2gmm(p=2) # 4 ports singed ended to 4 ports mixed mode

        #Return Loss
        net.s11.plot_s_db(label=f"{f}: Sdd11 (Return Loss)", linestyle='--')

        #@ Nyquist Frequency
        idx_14G = (np.abs(net.f - 14e9)).argmin()
        loss_14G = net.s11.s_db[idx_14G, 0, 0]
        print(f"{f}: Loss @14GHz = {loss_14G:.2f} dB")
    except FileNotFoundError:
        print(f"Error: Could not find {f}")

plt.axvline(x=14e9, c='r', linestyle='--', label='Nyquist (14GHz)')
plt.title("Differential S-Parameters: Return Loss (Sdd11)")
plt.xlabel("Frequency (GHz)")
plt.ylabel("Magnitude (dB)")
plt.grid(True, axis='both', linestyle=':', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()