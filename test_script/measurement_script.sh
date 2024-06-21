#!/bin/bash

# Network Test Collection Script
#
# Description:
# This script is designed to automate network performance tests using `iperf3` and a CLI application.
# It collects data and logs the results to a specified directory. The script can be easily customized
# and integrated into any network testing routine.
#
# Usage:
# ./script_name.sh point_name [log_directory]
#   point_name: Required. The name of the point to log.
#   log_directory: Optional. The directory to store the logs. Defaults to the current directory if not provided.
#
# Script Details:
# Variables:
#   POINT_NAME: The name of the point provided as an argument.
#   SERVER_IP: The IP address of the `iperf3` server. Default is `192.168.200.1`.
#   IPERF3_DURATION: Duration of the `iperf3` test in seconds. Default is `30`.
#   BW: Bandwidth setting. Default is `2` (can be adjusted as needed).
#   LOG_DIR: The directory where logs will be stored. Defaults to the current directory.
#   CURRENT_DIR: The current working directory.
#   DEFAULT_LOG_DIR: The default directory for storing logs. Can be changed by modifying the variable at the beginning of the script.
#   OUTPUT_FILE: The file where the log will be saved.
#
# Functions:
# 1. `usage`: Displays the usage information.
# 2. `run_iperf3_test`: Runs the `iperf3` test and logs the results.
# 3. `run_cli_test`: Runs the CLI test and logs the results.
# 4. `main`: The main function that orchestrates the tests and logging.
#
# Execution:
# The script begins execution by checking if the `point_name` argument is provided. If not, it displays
# the usage information and exits. It then sets up the required variables and functions before running the
# `main` function, which handles directory creation, logging, and running the tests.
#
# Example Usage:
# 1. Using the default log directory:
#    ./script_name.sh my_test_point
#    This will save the logs in the current directory.
#
# 2. Specifying a log directory:
#    ./script_name.sh my_test_point /path/to/log_directory
#    This will save the logs in `/path/to/log_directory`.
#
# Customization:
# - Default Log Directory: You can change the `DEFAULT_LOG_DIR` variable at the beginning of the script to set
#   a different default log directory.
# - Server IP: Modify the `SERVER_IP` variable to match the IP address of your `iperf3` server.
# - Test Duration and Bandwidth: Adjust `IPERF3_DURATION` and `BW` as needed for your tests.
#
# Notes:
# - Ensure `iperf3` and the required CLI application (`cli_app` and `cli_test.sh`) are installed and accessible.
# - The script assumes a specific directory structure for the CLI application (`nrc_pkg/script/`). Adjust paths
#   as necessary to match your setup.

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
POINT_NAME="$1"                 # Point name provided as an argument
SERVER_IP="192.168.200.1"       # IP address of the iperf3 server
IPERF3_DURATION=30              # Duration of the iperf3 test in seconds
BW=2                            # Bandwidth setting (can be adjusted)
LOG_DIR="${2:-$DEFAULT_LOG_DIR}"# Log directory, defaulting to the specified default log directory if not provided
CURRENT_DIR=$(pwd)              # Get the current directory

# Function to run iperf3 test
run_iperf3_test() {
    echo "Running iperf3 test for $IPERF3_DURATION seconds..." | tee -a "$OUTPUT_FILE"
    echo -e "\n*** iperf3 Test ***" | tee -a "$OUTPUT_FILE"
    iperf3 -c "$SERVER_IP" -u -b 0 -t "$IPERF3_DURATION" | tee -a "$OUTPUT_FILE"
}

# Function to run CLI test
run_cli_test() {
    echo "Running CLI test..." | tee -a "$OUTPUT_FILE"
    cd "$CURRENT_DIR/nrc_pkg/script/" || exit
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
