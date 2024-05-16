import pandas as pd
import glob

# Path to the directory containing the CSV files
path = '/data/indoor/'

# Get a list of all CSV files in the directory
csv_files = glob.glob(path + "*.csv")

# Initialize a list to store the aggregated data
data = []

# Read each CSV file
for file in csv_files:
    df = pd.read_csv(file)

    # Extract the scenario characteristics (assuming the first row has these details)
    scenario = {
        'Test Name': df.loc[0, 'Test Name'],
        'MCS': df.loc[0, 'MCS'],
        'BW': df.loc[0, 'Bandwidth'],
        'Freq': df.loc[0, 'Frequency'],
        'Rate Control': df.loc[0, 'Rate Control'],
        'GI': df.loc[0, 'Guard Interval'],
        'Tx Gain': df.loc[0, 'Tx Gain'],
        'Packet Size': df.loc[0, 'Packet Size'],
        'Packets Transmitted': df.loc[0, 'Packets Transmitted'],
        'Packets Received': df.loc[0, 'Packets Received'],
        'Packet Loss (%)': df.loc[0, 'Packet Loss (%)'],
        'Test Length (seconds)': df.loc[0, 'Test Length (seconds)'], # iperf3 time
        'Receiver Lost/Total Datagrams': df.loc[0, 'Receiver Lost/Total Datagrams'],
        'Jitter': df.loc[0, 'Jitter'],
        'Receiver BER (%)': df.loc[0, 'Receiver BER (%)'],
        'RSSI Sequence Index': df.loc[0, 'RSSI Sequence Index'],
        'Sequence': df.loc[0, 'Sequence'],
        'Time': df.loc[0, 'Time'],
        'SNR': df.loc[0, 'SNR'],
        'RSSI': df.loc[0, 'RSSI'],

        # Add other scenario characteristics as needed
    }

    # Extract lists of the measurements
    scenario['RSSI'] = df['RSSI'].dropna().tolist()
    scenario['SNR'] = df['SNR'].dropna().tolist()
    scenario['Iperf Bitrate (Mbits/sec)'] = df['Iperf Bitrate (Mbits/sec)'].dropna().tolist()
    scenario['Ping Time (ms)'] = df['Ping Time (ms)'].dropna().tolist() if 'Ping Time (ms)' in df.columns else []

    # Append the scenario data to the list
    data.append(scenario)

# Create a DataFrame from the aggregated data
combined_df = pd.DataFrame(data)

# Display the combined DataFrame
print(combined_df)
