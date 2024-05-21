import numpy as np


class Scenario:    
    def __init__(self, test_name, test_type, distance, attenuation, propagation, bandwidth, frequency, mcs, rate_control, guard_interval, tx_gain, 
                iperf_test_length, rx_iperf_bitrate, tx_iperf_bitrate, receiver_lost_total_datagrams, jitter, 
                receiver_ber, rssi_sequence,snr_sequence 
                ):
        self.test_name = test_name
        self.test_type = test_type              # 'coaxial', 'indoor' or 'outdoor'
        self.distance = distance                # distance in meters, null for coaxial
        self.attenuation = attenuation          # attenuation in dB for coaxial, null for indoor and outdoor
        self.propagation = propagation          # 'LoS' or 'NLoS'
        self.bandwidth = bandwidth              # '1' or '2' MHz
        self.frequency = frequency              # Channel used
        self.mcs = mcs 
        self.rate_control = rate_control        # 'on' or 'off'
        self.guard_interval = guard_interval    # 'short' or 'long'
        self.tx_gain = tx_gain                  # 'high' or 'low'
        self.iperf_test_length = iperf_test_length # in seconds
        self.receiver_lost_total_datagrams = receiver_lost_total_datagrams 
        self.jitter = jitter                    # in ms
        self.receiver_ber = receiver_ber        # in %
        self.rssi_sequence = rssi_sequence      # list of RSSI values 
        self.snr_sequence = snr_sequence         # list of SNR values 
        self.rx_iperf_bitrate = rx_iperf_bitrate      # in Mbits/sec
        self.tx_iperf_bitrate = tx_iperf_bitrate      # in Mbits/sec

        self.snr = np.average(snr_sequence)     # should use median value?
        self.rssi = np.average(rssi_sequence)   # should use median value?