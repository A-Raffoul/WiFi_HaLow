import re
import pandas as pd
import os

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

def extract_test_name(base_name, test_type):
    parts = base_name.split('_')
    return '_'.join(parts[:2]) + '_' + test_type

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

def extract_ping_data(log_content):
    ping_packet_loss_pattern = re.compile(r"(\d+\.\d+)% packet loss")
    rtt_pattern = re.compile(r"rtt min/avg/max/mdev = ([\d\.]+)/([\d\.]+)/([\d\.]+)/([\d\.]+) ms")
    ping_time_pattern = re.compile(r"time=(\d+\.?\d*) ms")
    unreachable_pattern = re.compile(r"Destination Host Unreachable")
    ping_packet_count_pattern = re.compile(r"Ping Packet Count: (\d+)")

    ping_packet_loss = ping_packet_loss_pattern.search(log_content).group(1) if ping_packet_loss_pattern.search(log_content) else None
    rtt_values = rtt_pattern.search(log_content).groups() if rtt_pattern.search(log_content) else None
    ping_times = ping_time_pattern.findall(log_content)
    unreachable_count = len(unreachable_pattern.findall(log_content))
    packets_transmitted = ping_packet_count_pattern.search(log_content).group(1) if ping_packet_count_pattern.search(log_content) else None
    ping_packets_received = len(ping_times)
    packet_size = 108  # Assuming 108 bytes as mentioned

    return ping_packet_loss, rtt_values, ping_times, unreachable_count, packets_transmitted, ping_packets_received, packet_size

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

def create_csv_data(test_name, mac_phy_data, ping_data, iperf_data, signal_data):
    mcs, bandwidth, frequency, rate_control, guard_interval, tx_gain = mac_phy_data
    ping_packet_loss, rtt_values, ping_times, unreachable_count, packets_transmitted, ping_packets_received, packet_size = ping_data
    iperf3_summary, bitrate_per_second = iperf_data
    rssi_values, snr_values = signal_data

    csv_data = {
        "Test Name": [test_name],
        "MCS": [mcs],
        "Bandwidth": [bandwidth],
        "Frequency": [frequency],
        "Rate Control": [rate_control],
        "Guard Interval": [guard_interval],
        "Tx Gain": [tx_gain],
        "Packet Size": [packet_size],
        "Packets Transmitted": [packets_transmitted],
        "Packets Received": [ping_packets_received],
        "Packet Loss (%)": [ping_packet_loss],
        "Ping Sequence": list(range(1, len(ping_times) + 1)),
        "Ping Time (ms)": ping_times,
        "Test Length (seconds)": [iperf3_summary.get("Test Length (seconds)")],
        "Receiver Bit Rate": [iperf3_summary.get("Receiver Bit Rate")],
        "Jitter": [iperf3_summary.get("Jitter")],
        "Receiver Lost/Total Datagrams": [iperf3_summary.get("Receiver Lost/Total Datagrams")],
        "Receiver BER (%)": [iperf3_summary.get("Receiver BER (%)")],
        "Iperf Second": list(range(1, len(bitrate_per_second) + 1)),
        "Iperf Bitrate (Mbits/sec)": bitrate_per_second,
        "RSSI Sequence Index": list(range(1, len(rssi_values) + 1)),
        "RSSI": rssi_values,
        "SNR": snr_values
    }

    return pd.DataFrame({key: pd.Series(value) for key, value in csv_data.items()})

def save_to_csv(csv_df, test_name, output_dir):
    file_name = f"{test_name}_results.csv"
    csv_file_path = os.path.join(output_dir, file_name)
    csv_df.to_csv(csv_file_path, index=False)
    print(f"CSV file created at: {csv_file_path}")

def process_log_file(log_file_path, output_dir='data', test_type='test'):
    base_name = os.path.splitext(os.path.basename(log_file_path))[0]
    test_name = extract_test_name(base_name, test_type)
    
    log_content = read_log_file(log_file_path)
    if not log_content:
        return

    mac_phy_data = extract_mac_phy_config(log_content)
    ping_data = extract_ping_data(log_content)
    iperf_data = extract_iperf_data(log_content)
    signal_data = extract_signal_info(log_content)
    
    csv_df = create_csv_data(test_name, mac_phy_data, ping_data, iperf_data, signal_data)
    save_to_csv(csv_df, test_name, output_dir)

def process_directory(log_files_dir, output_dir, test_type='test'):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_files_dir_abs = os.path.join(script_dir, log_files_dir)
    output_dir_abs = os.path.join(script_dir, output_dir)
    os.makedirs(output_dir_abs, exist_ok=True)

    for root, dirs, files in os.walk(log_files_dir_abs):
        for file in files:
            if file.endswith('.log'):
                file_path = os.path.join(root, file)
                try:
                    process_log_file(file_path, output_dir_abs, test_type)
                    # print(f"Processed file: {file}")
                except Exception as e:
                    print(f"An error occurred while processing {file}: {e}")

    print("Success")