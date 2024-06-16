#!/bin/bash

# Check if the point name is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 point_name"
    exit 1
fi

# Variables
POINT_NAME="$1"            # Point name provided as argument
SERVER_IP="192.168.200.1"  # Replace with the IP address of the iperf3 server (AP IP address)
IPERF3_DURATION=30         # Duration of iperf3 test in seconds
SIGNAL_LENGTH=100
BW=2


# Function to run iperf3 test
run_iperf3_test() {
    echo "Running iperf3 test for $IPERF3_DURATION seconds..." | tee -a $OUTPUT_FILE
    echo -e "\n*** iperf3 Test ***" | tee -a $OUTPUT_FILE
    iperf3 -c "$SERVER_IP" -u -b 0 -t "$IPERF3_DURATION" | tee -a $OUTPUT_FILE
}

# Function to run ping test
run_ping_test() {
    echo "\n Running ping test with $PING_COUNT packets..." | tee -a $OUTPUT_FILE
    echo -e "\n*** Ping Test ***" | tee -a $OUTPUT_FILE
    ping -c "$PING_COUNT" -i 1 -s "$PACKET_SIZE" "$SERVER_IP"  | tee -a $OUTPUT_FILE
}

run_cli_test() {
    cd ~/nrc_pkg/script/
    echo "\n Running CLI test..." | tee -a $OUTPUT_FILE
    ./cli_app show config | tee -a $OUTPUT_FILE
    cd ~/Desktop
    ./cli_test.sh | tee -a $OUTPUT_FILE
}

# Main Function
main() {



    LOG_DIR="/home/pi/Desktop/Outdoor_meas/LOS_${BW}MHz"

    # Create the directory if it doesn't already exist
    mkdir -p "$LOG_DIR"

    OUTPUT_FILE="/home/pi/Desktop/Outdoor_meas/LOS_${BW}MHz/${POINT_NAME}_${BW}Mhz_outdoor_$(date +%H%M).log"

    cd ~/nrc_pkg/script/
    echo "Starting Network Test Collection..." | tee -a $OUTPUT_FILE
    echo "Timestamp: $(date)" | tee -a $OUTPUT_FILE
    echo "iperf3 Server IP: $SERVER_IP" | tee -a $OUTPUT_FILE
    echo "iperf3 Test Duration: $IPERF3_DURATION seconds" | tee -a $OUTPUT_FILE
    echo "Ping Packet Count: $PING_COUNT" | tee -a $OUTPUT_FILE
    
    run_iperf3_test
    run_cli_test
    
    echo -e "\nNetwork test collection completed." | tee -a $OUTPUT_FILE
    echo "Results saved to $OUTPUT_FILE."
}

# Run the main function
main


