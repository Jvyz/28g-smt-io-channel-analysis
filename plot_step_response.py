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
    
    #port reordering 
    net.renumber(from_ports=[0, 2, 1, 3], to_ports=[0, 1, 2, 3])

    #mixed mode/differential conversion
    net.se2gmm(p=2)
    net.renormalize(100) #doesn't change anything but I note it anyways
    
    #sdd21 calculation
    sdd21 = net.s[:, 1, 0] 
    
    #convert to one port for skrf functions
    net_sdd21 = rf.Network(frequency=net.frequency, s=sdd21)
    
    #extrapolation to DC
    net_dc = net_sdd21.extrapolate_to_dc(kind='linear', dc_sparam=1.0)
    
    #step responsee calculation
    t, step = net_dc.step_response(window='hamming', pad=2000)

    #plot
    plt.plot(t * 1e9, step, label=f"{label} Thru", linewidth=2)

plt.title("Differential Step Response")
plt.xlabel("Time (ns)")
plt.ylabel("Voltage (Normalized)")
plt.axhline(1.0, color='r', linestyle='--', alpha=0.3, label="Ideal Thru")
plt.ylim(-0.1, 1.2)
plt.legend()
plt.grid(True)
plt.show()