import os
import pandas as pd

import matplotlib.pyplot as plt

# Path to the directory containing the CSV files
directory = 'data/indoor'

# Get a list of all CSV files in the directory
csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]

# Process each CSV file
for file in csv_files:
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(os.path.join(directory, file))

    # Extract the relevant columns for throughput, SNR, and RSSI
    throughput = df['Iperf Bitrate (Mbits/sec)']
    iperf_second = df['Iperf Second']
    snr = df['SNR']
    rssi = df['RSSI']
    time = df['RSSI Sequence Index']

    # Plot throughput vs time
    # plt.figure()
    # plt.plot(iperf_second, throughput)
    # plt.xlabel('Time')
    # plt.ylabel('Throughput')
    # plt.title('Throughput vs Time')

    # # Plot SNR vs time
    # plt.figure()
    # plt.plot(time, snr)
    # plt.xlabel('Time')
    # plt.ylabel('SNR')
    # plt.title('SNR vs Time')

    # # Plot RSSI vs time
    # plt.figure()
    # plt.plot(time, rssi)
    # plt.xlabel('Time')
    # plt.ylabel('RSSI')
    # plt.title('RSSI vs Time')
    # plt.show()

    # Show the plots
    


import plotly.graph_objects as go

# Create a trace for SNR
trace_snr = go.Scatter(
    x = time,
    y = snr,
    mode = 'lines',
    name = 'SNR'
)

# Create a trace for RSSI
trace_rssi = go.Scatter(
    x = time,
    y = rssi,
    mode = 'lines',
    name = 'RSSI'
)

# Create a trace for throughput
trace_tp = go.Scatter(
    x = time,
    y = throughput,
    mode = 'lines',
    name = 'Throughput'
)

# Create a list to store all the traces
traces = [trace_snr, trace_rssi, trace_tp]



# Process each CSV file
for file in csv_files:
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(os.path.join(directory, file))

    # Extract the relevant columns for throughput, SNR, and RSSI
    throughput = df['Iperf Bitrate (Mbits/sec)']
    iperf_second = df['Iperf Second']
    snr = df['SNR']
    rssi = df['RSSI']
    time = df['RSSI Sequence Index']

    # # Create a trace for RSSI for each file
    # trace_rssi = go.Scatter(
    #     x = time,
    #     y = rssi,
    #     mode = 'lines',
    #     name = f'RSSI - {file}'  # Use the file name as the trace name
    # )

    # Add the trace to the list of traces
    traces.append(trace_rssi)
    # Create a trace for throughput for each file
    trace_tp = go.Scatter(
        x = iperf_second,
        y = throughput,
        mode = 'lines',
        name = f'Throughput - {file}'  # Use the file name as the trace name
    )

    # Add the trace to the list of traces
    traces.append(trace_tp)

# Create a layout
layout = go.Layout(
    title = 'Throughput Information',
    xaxis = dict(title = 'Time'),
    yaxis = dict(title = 'Value'),
)

# Create a figure and add traces
fig = go.Figure(data=traces, layout=layout)

# Show the figure
fig.show()
# Path: extract_data.py