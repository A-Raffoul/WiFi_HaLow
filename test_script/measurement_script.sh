#!/bin/bash

# Default log directory (can be changed here)
DEFAULT_LOG_DIR="$(pwd)"

# Function to display usage
usage() {
    echo "Usage: $0 point_name [log_directory]"
    echo "  point_name: The name of the point to log."
    echo "  log_directory: Optional. The directory to store the logs. Defaults to the specified default log directory."
    exit 1
}

# Check if the point name is provided as an argument
if [ -z "$1" ]; then
    usage
fi

# Variables
POINT_NAME="$1"                  # Point name provided as an argument
SERVER_IP="192.168.200.1"        # IP address of the iperf3 server
IPERF3_DURATION=30               # Duration of the iperf3 test in seconds
BW=2                             # Bandwidth setting (can be adjusted)
LOG_DIR="${2:-$DEFAULT_LOG_DIR}" # Log directory, defaulting to the specified default log directory if not provided
CURRENT_DIR=$(pwd)               # Get the current directory

# Function to run iperf3 test
run_iperf3_test() {
    echo "Running iperf3 test for $IPERF3_DURATION seconds..." | tee -a "$OUTPUT_FILE"
    echo -e "\n*** iperf3 Test ***" | tee -a "$OUTPUT_FILE"
    iperf3 -c "$SERVER_IP" -u -b 0 -t "$IPERF3_DURATION" | tee -a "$OUTPUT_FILE"
}

# Function to run CLI test
run_cli_test() {
    echo "Running CLI test..." | tee -a "$OUTPUT_FILE"
    cd "~/nrc_pkg/script/" || exit
    ./cli_app show config | tee -a "$OUTPUT_FILE"
    cd "$CURRENT_DIR" || exit
    ./cli_test.sh | tee -a "$OUTPUT_FILE"
}

# Main Function
main() {
    # Create the log directory if it doesn't exist
    mkdir -p "$LOG_DIR"
    
    # Set output file path
    OUTPUT_FILE="$LOG_DIR/${POINT_NAME}_${BW}Mhz_outdoor_$(date +%H%M).log"

    # Begin logging
    echo "Starting Network Test Collection..." | tee -a "$OUTPUT_FILE"
    echo "Timestamp: $(date)" | tee -a "$OUTPUT_FILE"
    echo "iperf3 Server IP: $SERVER_IP" | tee -a "$OUTPUT_FILE"
    echo "iperf3 Test Duration: $IPERF3_DURATION seconds" | tee -a "$OUTPUT_FILE"

    # Run the tests
    run_iperf3_test

    run_cli_test

    # Completion message
    echo -e "\nNetwork test collection completed." | tee -a "$OUTPUT_FILE"
    echo "Results saved to $OUTPUT_FILE."
}

# Run the main function
main
