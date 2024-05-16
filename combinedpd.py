import pandas as pd
import glob
import os


# Path to the directory containing the CSV files


# directory = 'data/indoor'
def read_csv_files(directory):    
    # Get a list of all CSV files in the directory
    csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]

    # Initialize a list to store the aggregated data
    data = []

    # Read each CSV file
    for file in csv_files:
        df = pd.read_csv(os.path.join(directory, file))

        # Extract the scenario characteristics (assuming the first row has these details)
        scenario = {
            # Test Name,MCS,Bandwidth,Frequency,Rate Control,Guard Interval,Tx Gain,
            # Packet Size,Packets Transmitted,Packets Received,Packet Loss (%),Ping Sequence,Ping Time (ms),
            # Test Length (seconds),Receiver Bit Rate,Jitter,Receiver Lost/Total Datagrams,Receiver BER (%),
            # Iperf Second,Iperf Bitrate (Mbits/sec),RSSI Sequence Index,RSSI,SNR

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

    # Return the combined DataFrame
    return combined_df
