import re
import os
from datetime import datetime
import numpy as np

def read_log_file(log_file_path):
    try:
        with open(log_file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {log_file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_mac_phy_config(log_content):
    mac_phy_config_pattern = re.compile(r"\[MAC Configuration\](.*?)\[PHY Configuration\](.*?)--", re.DOTALL)
    mac_phy_config_match = mac_phy_config_pattern.search(log_content)

    if not mac_phy_config_match:
        return None, None, None, None, None, None

    mac_config = mac_phy_config_match.group(1)
    phy_config = mac_phy_config_match.group(2)

    mcs_pattern = re.compile(r"-MCS\s+:\s+(\d+)")
    bandwidth_pattern = re.compile(r"Bandwidth\s+:\s+(\d+\w?)")
    frequency_pattern = re.compile(r"Frequency\s+:\s+(\d+)")
    rate_control_pattern = re.compile(r"Rate Control\s+:\s+(ON|OFF)")
    guard_interval_pattern = re.compile(r"Guard Interval\s+:\s+(LONG|SHORT)")
    tx_gain_pattern = re.compile(r"TX_Gain\s+:\s+(\d+)")

    mcs = mcs_pattern.search(mac_config).group(1) if mcs_pattern.search(mac_config) else None
    bandwidth = bandwidth_pattern.search(mac_config).group(1) if bandwidth_pattern.search(mac_config) else None
    frequency = frequency_pattern.search(mac_config).group(1) if frequency_pattern.search(mac_config) else None
    rate_control = rate_control_pattern.search(mac_config).group(1) if rate_control_pattern.search(mac_config) else None
    guard_interval = guard_interval_pattern.search(mac_config).group(1) if guard_interval_pattern.search(mac_config) else None
    tx_gain = tx_gain_pattern.search(phy_config).group(1) if tx_gain_pattern.search(phy_config) else None

    return mcs, bandwidth, frequency, rate_control, guard_interval, tx_gain

def extract_iperf_data(log_content):
    iperf3_pattern = re.compile(r"\*\*\* iperf3 Test \*\*\*(.*?)iperf Done.", re.DOTALL)
    iperf3_match = iperf3_pattern.search(log_content)

    if not iperf3_match:
        return {}, []

    iperf3_results = iperf3_match.group(1)

    summary_pattern = re.compile(
        r"\[\s*\d+\]\s+\d+\.\d+-\d+\.\d+\s+sec\s+[\d\.]+\s+\w*Bytes\s+([\d\.]+)\s+(K|M|)bits/sec\s+([\d\.]+)\s+ms\s+(\d+)/(\d+)\s+\(([\d\.]+)%\)\s+(sender|receiver)"
    )
    summary_match = summary_pattern.findall(iperf3_results)

    iperf3_summary = {}
    for match in summary_match:
        receiver_bit_rate = float(match[0])
        if match[1] == "K":
            receiver_bit_rate /= 1000  # Convert Kbits/sec to Mbits/sec
        iperf3_summary = {
            "Test Length (seconds)": 60,  # Assuming 60 seconds as mentioned
            "Receiver Bit Rate": receiver_bit_rate,
            "Jitter": match[2],
            "Receiver Lost/Total Datagrams": f"{match[3]}/{match[4]}",
            "Receiver BER (%)": match[5]
        }

    bitrate_per_second = []
    detailed_lines = iperf3_results.splitlines()
    bitrate_pattern = re.compile(
        r"\[\s*\d+\]\s+\d+\.\d+-\d+\.\d+\s+sec\s+([\d\.]+)\s+\w*Bytes\s+([\d\.]+)\s+(K|M|)bits/sec"
    )
    
    for line in detailed_lines:
        if "sender" in line or "receiver" in line:
            continue  # Skip summary lines
        match = bitrate_pattern.search(line)
        if match:
            groups = match.groups()
            bitrate = float(groups[1])
            if groups[2] == "K":
                bitrate /= 1000  # Convert Kbits/sec to Mbits/sec
            bitrate_per_second.append(bitrate)

    return iperf3_summary, bitrate_per_second

def extract_signal_info(log_content):
    signal_info_pattern = re.compile(r"Mac Addr\s+: \S+\s+rssi: (-?\d+)\s+snr: (\d+)")
    signal_matches = signal_info_pattern.findall(log_content)

    rssi_values = [int(match[0]) for match in signal_matches]
    snr_values = [int(match[1]) for match in signal_matches]

    return rssi_values, snr_values

def extract_timestamp_and_attenuation(log_content):
    timestamp_pattern = re.compile(r"Timestamp\s*:\s*(.+)")
    attenuation_pattern = re.compile(r"Coaxial set up with (\d+) dBm attenuation")

    timestamp_match = timestamp_pattern.search(log_content)
    attenuation_match = attenuation_pattern.search(log_content)

    timestamp = timestamp_match.group(1) if timestamp_match else None
    attenuation = attenuation_match.group(1) if attenuation_match else None

    return timestamp, attenuation

def create_text_data(test_name, mac_phy_data, iperf_data, signal_data, timestamp, attenuation):
    mcs, bandwidth, frequency, rate_control, guard_interval, tx_gain = mac_phy_data
    iperf3_summary, _ = iperf_data
    rssi_values, snr_values = signal_data

    text_data = f"""test_name: {test_name}
timestamp: {timestamp}
test_type: coaxial
distance: null
attenuation: {attenuation}
propagation: LoS
bandwidth: {bandwidth}
frequency: {frequency}
mcs: {mcs}
rate_control: {rate_control.lower()}
guard_interval: {guard_interval.lower()}
tx_gain: {tx_gain}
iperf_test_length: {iperf3_summary.get("Test Length (seconds)")}
rx_iperf_bitrate: {iperf3_summary.get("Receiver Bit Rate")}
tx_iperf_bitrate: {iperf3_summary.get("Receiver Bit Rate")}
receiver_lost_total_datagrams: {iperf3_summary.get("Receiver Lost/Total Datagrams")}
jitter: {iperf3_summary.get("Jitter")}
receiver_ber: {iperf3_summary.get("Receiver BER (%)")}
rssi_sequence: {rssi_values}
snr_sequence: {snr_values}
rsii : {np.median(rssi_values)}
snr : {np.median(snr_values)}
"""

    return text_data

def save_to_text(text_data, test_name, output_dir):
    clean_test_name = test_name.replace("_combined", "")
    file_name = f"{clean_test_name}.txt"    
    text_file_path = os.path.join(output_dir, file_name)
    with open(text_file_path, 'w') as file:
        file.write(text_data)
    print(f"Text file created at: {text_file_path}")

def process_log_file(log_file_path, output_dir='data'):
    base_name = os.path.splitext(os.path.basename(log_file_path))[0]
    
    log_content = read_log_file(log_file_path)
    if not log_content:
        return

    mac_phy_data = extract_mac_phy_config(log_content)
    iperf_data = extract_iperf_data(log_content)
    signal_data = extract_signal_info(log_content)
    timestamp, attenuation = extract_timestamp_and_attenuation(log_content)
    
    text_data = create_text_data(base_name, mac_phy_data, iperf_data, signal_data, timestamp, attenuation)
    save_to_text(text_data, base_name, output_dir)

def process_directory(log_files_dir, output_dir):
    log_files_dir_abs = os.path.abspath(log_files_dir)
    output_dir_abs = os.path.abspath(output_dir)
    os.makedirs(output_dir_abs, exist_ok=True)

    for root, dirs, files in os.walk(log_files_dir_abs):
        for dir in dirs:
            source_dir = os.path.join(root, dir)
            target_dir = os.path.join(output_dir_abs, dir)
            os.makedirs(target_dir, exist_ok=True)

            for file in os.listdir(source_dir):
                if file.endswith('.log'):
                    file_path = os.path.join(source_dir, file)
                    try:
                        process_log_file(file_path, target_dir)
                        print(f"Processed file: {file}")
                    except Exception as e:
                        print(f"An error occurred while processing {file}: {e}")

    print("Processing complete.")

# Example usage
source_directory = r'C:\Users\raffoul\Desktop\WiFi_HaLow\data\coaxial\raw-logs'
target_directory = r'C:\Users\raffoul\Desktop\WiFi_HaLow\data\coaxial\logs'
process_directory(source_directory, target_directory)