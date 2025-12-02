import skrf as rf
import matplotlib.pyplot as plt
import numpy as np

files = [
    "TEC_SMT_IO_42GHz_Thru_B5B6_4in.s4p",
    "TEC_SMT_IO_42GHz_Thru_B5B6_10in.s4p"
]

plt.figure(figsize=(10, 6))

for f in files:
    try:
        net = rf.Network(f)
    except FileNotFoundError:
        print(f"Error: Could not find {f}")
        continue

    net.renumber(from_ports=[0, 2, 1, 3], to_ports=[0, 1, 2, 3])
    net.se2gmm(p=2) # 4 ports singed ended to 4 ports mixed mode
    net.renormalize(100)
    
    net.plot_s_db(m=1, n=0, label=f"{f} (Sdd21)")

    freq_point = 14e9
    idx = (np.abs(net.f - freq_point)).argmin()
    loss = net.s_db[idx, 1, 0]
    
    print(f"{f}: Loss @ 14GHz = {loss:.2f} dB")

plt.axvline(x=14e9, c='r', linestyle='--', label='Nyquist (14GHz)')
plt.title("Differential Insertion Loss (Sdd21)")
plt.xlabel("Frequency (GHz)")
plt.ylabel("Magnitude (dB)")
plt.ylim(-30, 2) # Zoom in to see the top clearly. 0dB is the max.
plt.grid(True, which='both', linestyle=':', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()