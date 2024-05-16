import re
import pandas as pd
import os

# Function to process a single log file and save it as a CSV
def process_log_file(log_file_path, output_dir):
    test_name = os.path.splitext(os.path.basename(log_file_path))[0]  # Use file name as test name
    try:
        with open(log_file_path, 'r') as file:
            log_content = file.read()
    except FileNotFoundError:
        print(f"File not found: {log_file_path}")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    # Extracting Test Configuration
    mac_phy_config_pattern = re.compile(r"\[MAC Configuration\](.*?)\[PHY Configuration\](.*?)--", re.DOTALL)
    mac_phy_config_match = mac_phy_config_pattern.search(log_content)

    mcs = bandwidth = frequency = rate_control = guard_interval = tx_gain = None

    if mac_phy_config_match:
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

    # Extracting Ping Test Data
    ping_packet_loss_pattern = re.compile(r"(\d+\.\d+)% packet loss")
    rtt_pattern = re.compile(r"rtt min/avg/max/mdev = ([\d\.]+)/([\d\.]+)/([\d\.]+)/([\d\.]+) ms")
    ping_time_pattern = re.compile(r"time=(\d+\.?\d*) ms")
    unreachable_pattern = re.compile(r"Destination Host Unreachable")

    ping_packet_loss = ping_packet_loss_pattern.search(log_content).group(1) if ping_packet_loss_pattern.search(log_content) else None
    rtt_values = rtt_pattern.search(log_content).groups() if rtt_pattern.search(log_content) else None
    ping_times = ping_time_pattern.findall(log_content)
    unreachable_count = len(unreachable_pattern.findall(log_content))

    ping_packet_count_pattern = re.compile(r"Ping Packet Count: (\d+)")
    packets_transmitted = ping_packet_count_pattern.search(log_content).group(1) if ping_packet_count_pattern.search(log_content) else None

    ping_packets_received = len(ping_times)
    packet_size = 108  # Assuming 108 bytes as mentioned

    # Extracting Iperf Test Data
    iperf3_pattern = re.compile(r"\*\*\* iperf3 Test \*\*\*(.*?)iperf Done.", re.DOTALL)
    iperf3_match = iperf3_pattern.search(log_content)

    iperf3_summary = {}
    bitrate_per_second = []

    if iperf3_match:
        iperf3_results = iperf3_match.group(1)

        # Extracting summary data
        summary_pattern = re.compile(
             r"\[\s*\d+\]\s+\d+\.\d+-\d+\.\d+\s+sec\s+\d+\.\d+\s+\w*Bytes\s+(\d+\.\d+)\s+(K|M|bits/sec)\s+(\d+\.\d+)\s+ms\s+(\d+)/(\d+)\s+\((\d+\.?\d*)%\)\s+(sender|receiver)"
        )
        summary_match = summary_pattern.findall(iperf3_results)
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

        # Extracting detailed bitrate per second data
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

        

    # Extracting RSSI and SNR
    signal_info_pattern = re.compile(r"Mac Addr\s+: \S+\s+rssi: (-?\d+)\s+snr: (\d+)")
    signal_matches = signal_info_pattern.findall(log_content)

    rssi_values = [int(match[0]) for match in signal_matches]
    snr_values = [int(match[1]) for match in signal_matches]

    # Creating the final structure
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

    # Converting to a DataFrame for CSV output
    csv_df = pd.DataFrame({key: pd.Series(value) for key, value in csv_data.items()})

    # Save the DataFrame to a CSV file
    file_name = f"{test_name}_results.csv"
    csv_file_path = os.path.join(output_dir, file_name)
    csv_df.to_csv(csv_file_path, index=False)

    print(f"CSV file created at: {csv_file_path}")

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Directory containing the log files
log_files_dir = os.path.join(script_dir, 'indoor_test')

# Directory to save the output CSV files
output_dir = os.path.join(script_dir, 'output_csvs')
os.makedirs(output_dir, exist_ok=True)

# Iterate over all files in the log files directory
for root, dirs, files in os.walk(log_files_dir):
    for file in files:
        if file.endswith('.log'):
            file_path = os.path.join(root, file)
            try:
                process_log_file(file_path, output_dir)
                print(f"Processed file: {file}")
            except Exception as e:
                print(f"An error occurred while processing {file}: {e}")

print("Success")
