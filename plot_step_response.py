import skrf as rf
import matplotlib.pyplot as plt
import numpy as np

files = {
    "4-inch": "TEC_SMT_IO_42GHz_Thru_B5B6_4in.s4p",
    "10-inch": "TEC_SMT_IO_42GHz_Thru_B5B6_10in.s4p"
}

plt.figure(figsize=(10, 6))

for label, f in files.items():
    # Load and convert to Differential (Mixed Mode)
    net = rf.Network(f)
    net.renormalize(50)
    net.se2gmm(p=2)
    
    # Extract Sdd21 (Differential Thru)
    # new 1-Port Network from just the Sdd21 data to use skrf's time tools
    sdd21 = net.s[:, 1, 0]  
    net_sdd21 = rf.Network(frequency=net.frequency, s=sdd21, z0=50)
    
    # extrapolate at 0Hz
    net_dc = net_sdd21.extrapolate_to_dc(kind='linear', dc_sparam=1.0)
    
    # 
    t, step = net_dc.step_response(window='hamming', pad=2000)
    
    # normalization
    step = step / np.max(step)
    
    #
    plt.plot(t * 1e9, step, label=f"{label} Step Response", linewidth=2)

plt.title("Channel Step Response (Corrected with DC & Windowing)")
plt.xlabel("Time (ns)")
plt.ylabel("Voltage (Normalized)")
plt.xlim(0, 2)
plt.grid(True)
plt.legend()
plt.show()