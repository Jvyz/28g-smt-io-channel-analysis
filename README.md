# 28g-smt-io-channel-analysis
Python script utilizing scikit-rf to plot and compare mixed-mode S-parameters for the 28 Gb/s SMT IO channel models (4-inch vs. 10-inch host) used in the IEEE P802.3bs (400GbE) Task Force analysis.

## Project Overview

Analyzing and verifying the electrical performance of high-speed interconnects used in the development of **IEEE P802.3bs (200 GbE and 400 GbE)** Ethernet standards.

The core analysis focuses on comparing the insertion loss and return loss of **28 Gb/s High Density SMT IO** channel models across different host PCB lengths.

## Methodology

The primary goal of this script is to assess the impact of host PCB trace length on signal integrity, specifically comparing the 4-inch host channel against the 10-inch host channel, which represents the longest supported electrical path. Following graphs are generated using Python:

![Eye Diagram of 10-inch Host Channels](result/eye_diagram_10.png)

![Eye Diagram of 4-inch Host Channels](result/eye_diagram_4.png)

![Comparison of Step Response for 4-inch and 10-inch Host Channels](result/step_response.png)

![Comparison of Sdd21 Loss for 4-inch and 10-inch Host Channels](result/insertion_loss.png)

TEC_SMT_IO_42GHz_Thru_B5B6_4in.s4p: Loss @14GHz = -4.67 dB

TEC_SMT_IO_42GHz_Thru_B5B6_10in.s4p: Loss @14GHz = -9.37 dB

![Comparison of Sdd11 Loss for 4-inch and 10-inch Host Channels](result/return_loss.png)

TEC_SMT_IO_42GHz_Thru_B5B6_4in.s4p: Loss @14GHz = -18.51 dB

TEC_SMT_IO_42GHz_Thru_B5B6_10in.s4p: Loss @14GHz = -27.80 dB

The Nyquist frequency for this analysis is **14 GHz** (based on 28 Gbaud signaling)

## Conclusion

The analysis provided insight on IEEE standards on high-speed protocol and signal integrity of 28Gb/s high density SMT IO, 4/10 inch host. Additioanlly, comprehensive measurements of mixed-mode S parameters were conducted and thus the performance were evaluated to better understand the standards of high-speed tranmission lines.

## Contribution
If you find issues or have suggestions for additional plots (e.g., Time Domain Reflectometry/TDR), feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.