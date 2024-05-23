import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Scenario:
    def __init__(self, file_path):
        self.file_path = file_path
        self.test_name = None
        self.timestamp = None
        self.test_type = None
        self.distance = None
        self.walls = None
        self.attenuation = 'null'
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
        self.receiver_lost_total_datagrams = None
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
                        self.distance = value
                    elif key == 'walls':
                        self.walls = value
                    elif key == 'attenuation':
                        self.attenuation = value
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
                    elif key == 'bit_rate_per_second':
                        self.bit_rate_per_second = [float(x) for x in re.findall(r'\d+\.\d+', value)]
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
