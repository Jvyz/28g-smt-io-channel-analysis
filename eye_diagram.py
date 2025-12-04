import skrf as rf
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import convolve

# --- CONFIGURATION ---
file_path = "TEC_SMT_IO_42GHz_Thru_B5B6_4in.s4p" 
data_rate = 28e9   # 28 Gbps NRZ
UI = 1 / data_rate # ~35.7 ps
num_bits = 3000    # More bits = smoother density
samples_per_symbol = 32 # 32 is usually enough for visual check

def run_eye_sim():
    try:
        net = rf.Network(file_path)
    except Exception:
        print("File not found.")
        return

    net.renumber(from_ports=[0, 2, 1, 3], to_ports=[0, 1, 2, 3])

    net.renormalize(50)
    net.se2gmm(p=2)
    
    sdd21 = net.s[:, 1, 0]
    
    #create a 1-port network of just the Sdd21 data
    net_sdd21 = rf.Network(frequency=net.frequency, s=sdd21, z0=100)
    
    #extrapolate to DC
    net_dc = net_sdd21.extrapolate_to_dc(kind='linear', dc_sparam=1.0)

    #automatically handles the frequency spacing and time axis
    t_impulse, impulse = net_dc.impulse_response(window='hamming', pad=2000)

    #resample Impulse to match Simulation Rate
    #we need strict timing for the convolution
    target_dt = UI / samples_per_symbol
    t_sim = np.arange(0, t_impulse[-1], target_dt)
    
    # Interpolate the impulse onto the new time grid
    impulse_interp = np.interp(t_sim, t_impulse, impulse)
    
    #normalize impulse energy so a steady '1' equals 1.0V
    #the sum of the impulse response * dt roughly equals the DC gain (1.0)
    current_area = np.sum(impulse_interp)
    impulse_interp = impulse_interp / current_area

    # 5. Generate Random Data
    bits = np.random.randint(0, 2, num_bits) * 2 - 1 # NRZ: -1, +1
    
    # 6. Transmit (Upsample + Convolve)
    tx_signal = np.repeat(bits, samples_per_symbol)
    rx_signal = convolve(tx_signal, impulse_interp)[:len(tx_signal)]

    # 7. Plotting
    plt.figure(figsize=(10, 6), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # Fold Logic
    fold_width = 2 * samples_per_symbol
    num_traces = len(rx_signal) // fold_width
    t_axis = np.linspace(0, 2, fold_width)
    
    # Plot traces
    for i in range(10, min(1000, num_traces)):
        segment = rx_signal[i*fold_width : (i+1)*fold_width]
        plt.plot(t_axis, segment, color='lime', alpha=0.2, linewidth=1)

    plt.title(f"28 Gbps Eye Diagram (10-inch Channel)", color='white')
    plt.xlabel("Time (UI)", color='white')
    plt.ylabel("Voltage (Normalized)", color='white')
    plt.xlim(0, 2)
    plt.ylim(-1.5, 1.5) # Center the eye
    plt.grid(False)
    plt.tick_params(colors='white')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_eye_sim()