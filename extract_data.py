import re
import pandas as pd
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the log file
log_file_path = os.path.join(script_dir, 'indoor_test', 'pointA_1Mhz_test08_0428.log')
# Load the log file content

## should see how to do it for several files
test_name = "Point_A_indoor_1MHz"

try:
    with open(log_file_path, 'r') as file:
        # Process the file
        data = file.read()
        # print(data)
except FileNotFoundError:
    print(f"File not found: {log_file_path}")
except Exception as e:
    print(f"An error occurred: {e}")

# Reading the file content
try:
    with open(log_file_path, 'r') as file:
        log_content = file.read()
except FileNotFoundError:
    print(f"File not found: {log_file_path}")
except Exception as e:
    print(f"An error occurred: {e}")

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
    summary_pattern = re.compile(r"\[.*?\]\s+\d+\.\d+-\d+\.\d+\s+sec\s+\d+\.\d+\s+MBytes\s+(\d+\.\d+)\s+Mbits/sec\s+(\d+\.\d+)\s+ms\s+(\d+)/(\d+)\s+\((\d+\.\d+)%\)\s+receiver")
    summary_match = summary_pattern.search(iperf3_results)
    if summary_match:
        summary_groups = summary_match.groups()
        iperf3_summary = {
            "Test Length (seconds)": 60,  # Assuming 60 seconds as mentioned
            "Receiver Bit Rate": summary_groups[0],
            "Jitter": summary_groups[1],
            "Receiver Lost/Total Datagrams": f"{summary_groups[2]}/{summary_groups[3]}",
            "Receiver BER (%)": summary_groups[4]
        }

    # Extracting detailed bitrate per second data
    bitrate_pattern = re.compile(r"\[\s*\d+\]\s+\d+\.\d+-\d+\.\d+\s+sec\s+\d+\s+KBytes\s+(\d+\.\d+)\s+Mbits/sec")
    bitrate_per_second = bitrate_pattern.findall(iperf3_results)

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
csv_file_path = os.path.join('data/indoor', file_name)
# csv_file_path = 'data/test_results.csv'
csv_df.to_csv(csv_file_path, index=False)

print(f"CSV file created at: {csv_file_path}")
print("success")