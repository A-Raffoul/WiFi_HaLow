import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, interactive, fixed, interact_manual


class Scenario:
    def __init__(self, file_path):
        self.file_path = file_path
        self.test_name = None
        self.timestamp = None
        self.test_type = None
        self.distance = 0
        self.walls = 0
        self.attenuation = 0
        self.propagation = 'LoS'
        self.bandwidth = None
        self.frequency = None
        self.mcs = None
        self.rate_control = 'null'
        self.guard_interval = 'null'
        self.tx_gain = None
        self.rx_iperf_bitrate = None
        self.tx_iperf_bitrate = None
        self.bit_rate_per_second = None
        self.receiver_lost_total_datagrams = 'null'
        self.jitter = None
        self.receiver_ber = None
        self.rssi_sequence = []
        self.snr_sequence = []
        self.rssi_median = None
        self.snr_median = None
        self.total_gain = None
        self.process_file()

    def process_file(self):
        with open(self.file_path, 'r') as file:
            for line in file:
                key_value = line.strip().split(': ', 1)
                if len(key_value) == 2:
                    key, value = key_value
                    if key == 'test_name':
                        self.test_name = value
                    elif key == 'timestamp':
                        self.timestamp = value
                    elif key == 'test_type':
                        self.test_type = value
                    elif key == 'distance':
                        if self.test_type == 'coaxial':
                            self.distance = 0
                        else:   
                            self.distance = int(value)
                    elif key == 'walls':
                        self.walls = int(value)
                    elif key == 'attenuation':
                        if self.test_type == 'coaxial':
                            self.attenuation = int(value)
                    elif key == 'propagation':
                        self.propagation = value
                    elif key == 'bandwidth':
                        self.bandwidth = value
                    elif key == 'frequency':
                        self.frequency = value
                    elif key == 'mcs':
                        self.mcs = int(value)
                    elif key == 'rate_control':
                        self.rate_control = value
                    elif key == 'guard_interval':
                        self.guard_interval = value
                    elif key == 'tx_gain':
                        self.tx_gain = int(value)
                    elif key == 'rx_iperf_bitrate':
                        self.rx_iperf_bitrate = float(value)
                    elif key == 'tx_iperf_bitrate':
                        self.tx_iperf_bitrate = float(value)
                    elif key == 'receiver_lost_total_datagrams':
                        self.receiver_lost_total_datagrams = value
                    # elif key == 'bit_rate_per_second':
                    #     self.bit_rate_per_second = [float(x) for x in re.findall(r'\d+\.\d+', value)]
                    elif key == 'jitter':
                        self.jitter = float(value)
                    elif key == 'receiver_ber':
                        self.receiver_ber = float(value)
                    elif key == 'rssi_sequence':
                        self.rssi_sequence = [int(x) for x in re.findall(r'-?\d+', value)]
                    elif key == 'snr_sequence':
                        self.snr_sequence = [int(x) for x in re.findall(r'\d+', value)]
                    elif key == 'rssi_median':
                        self.rssi_median = float(value)
                    elif key == 'snr_median':
                        self.snr_median = float(value)

        if self.test_type == 'coaxial':
            self.total_gain = self.tx_gain - self.attenuation
        

    def to_dict(self):
        return {
            'Test Name': self.test_name,
            'Timestamp': self.timestamp,
            'Test Type': self.test_type,
            'Distance': self.distance,
            'Walls': self.walls,
            'Attenuation (dBm)': self.attenuation,
            'Propagation': self.propagation,
            'Bandwidth': self.bandwidth,
            'Frequency': self.frequency,
            'MCS': self.mcs,
            'Rate Control': self.rate_control,
            'Guard Interval': self.guard_interval,
            'TX Gain': self.tx_gain,
            'RX iPerf Bitrate (Mbits/sec)': self.rx_iperf_bitrate,
            'TX iPerf Bitrate (Mbits/sec)': self.tx_iperf_bitrate,
            'Receiver Lost/Total Datagrams': self.receiver_lost_total_datagrams,
            'Jitter (ms)': self.jitter,
            'Receiver BER (%)': self.receiver_ber,
            'RSSI Median': self.rssi_median,
            'SNR Median': self.snr_median,
            'Total Gain' : self.total_gain
        }
    


# Function to extract scenarios from text files

def extract_scenarios_from_text_files(directory):
    scenarios = []
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            source_dir = os.path.join(root, dir)
            for file in os.listdir(source_dir):
                print(file)
                if file.endswith('.txt'):
                    file_path = os.path.join(source_dir, file)
                    try:
                        scenario = Scenario(file_path)
                        scenarios.append(scenario)
                    except Exception as e:
                        print(f"An error occurred while processing {file_path}: {e}")
                        continue
        for file in os.listdir(directory):
                print(file)
                if file.endswith('.txt'):
                    file_path = os.path.join(directory, file)
                    try:
                        scenario = Scenario(file_path)
                        scenarios.append(scenario)
                    except Exception as e:
                        print(f"An error occurred while processing {file_path}: {e}")
                        continue
    return scenarios

def scenarios_to_dataframe(scenarios):
    data_dicts = [scenario.to_dict() for scenario in scenarios]
    return pd.DataFrame(data_dicts)

def get_average_and_std(df, group_by, value):
    average = df.groupby(group_by)[value].mean().reset_index()
    std = df.groupby(group_by)[value].std().reset_index()
    return average, std

def plot_interactive(df):
    def update_plot(x, y):
        fig = px.scatter(df, x=x, y=y, title=f'{x} vs {y}', labels={x: x, y: y})
        fig.show()

    columns = df.columns
    interact(update_plot, x=columns, y=columns)

