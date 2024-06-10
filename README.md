# WiFi_HaLow

Welcome to the WiFi_HaLow repository! This project is a part of a semester-long effort to analyze and visualize network performance data. 
This project was led by Tony Raffoul (EPFL) and Francesco Murande Escobar (EPFL) under the supervision of Prof. Andreas Burg within the Telecommunications and Circuits Lab at EPFL and the help of Mr. Herman Huni. 
The primary focus was on characterizing the capabilities of the WiFi HaLow network under the Swiss/EU regulations.

In this repository, you can also find the project report, presentation slide, as well as all the software used for the project.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Data Extraction](#data-extraction)
4. [Data Processing](#data-processing)
5. [Visualization](#visualization)


## Introduction

WiFi_HaLow is a comprehensive tool designed to handle network performance data efficiently. This repository serves as a framework to:
- Process network performance test files.
- Extract crucial data metrics.
- Visualize the data for analysis.

## Features

- **Data Extraction:** Efficiently extracts Iperf3 data, RSSI, SNR, and ping RTT time from test files.
- **Data Processing:** Organizes extracted data into a scenario class for structured analysis.
- **Visualization:** Provides tools for visualizing the network performance metrics for better insight.

## Data Extraction

The first step is to process the raw test files using `log_cleaner.py`. You can configure the target and source directory and specify the test type (e.g., coaxial, outdoor, indoor). The script processes the files based on the information encoded in the file names, such as floor difference (floor_x) and distance (dist_x).

The raw log files are transformed into easier-to-process text files. Below is an example of a typical processed log file:

```
test_name: dist_0m_1M_1Mhz_outdoor_1751
timestamp: Tue 28 May 2024 05:51:41 PM -01
test_type: outdoor
distance: 0
walls: 0
attenuation: None
propagation: NLoS
bandwidth: 1M
frequency: 8655
mcs: 7
rate_control: on
guard_interval: long
tx_gain: 14
iperf_test_length: 60
rx_iperf_bitrate: 1.84
tx_iperf_bitrate: 1.86
bit_rate_per_second: [2.55, 1.74, 1.85, 1.85, 1.74, 1.74, 1.85, 1.85, 1.74, 1.85, 1.85, 1.74, 1.85, 1.97, 1.85, 1.74, 1.97, 1.74, 1.97, 1.74, 1.85, 1.85, 1.85, 1.85, 1.85, 1.85, 1.85, 1.85, 1.85, 1.97]
receiver_lost_total_datagrams: 0/4820
jitter: 9.116
receiver_ber: 0
rssi_sequence: [-46, -45, -45, -45, -45, -45, -45, -45, -45, -45, -45, -46]
snr_sequence: [29, 29, 28, 28, 28, 29, 29, 28, 28, 28, 29, 28]
rssi_median: -45.0
snr_median: 28.0
```


## Data Processing

The processed text files are then handled by `scenario.py`, which defines the `Scenario` class. This class reads each text file and processes the information into a structured format. The data is then compiled into a DataFrame, facilitating easy visualization and further analysis.

## Visualization

We provide an example notebook, `data_visualization.ipynb`, which demonstrates the typical use of the library. This notebook was used to create most of the graphs during the course of this project. It serves as a practical guide for visualizing the network performance metrics and gaining insights from the data.

