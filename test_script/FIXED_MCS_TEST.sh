
#!/bin/bash

# Variables
SERVER_IP="192.168.200.1"  # Replace with the IP address of the iperf3 server (AP IP address)
IPERF3_DURATION=30      # Duration of iperf3 test in seconds
PING_COUNT=20           # Number of ping packets
PACKET_SIZE=100		 # number of bytes sent
SIGNAL_LENGTH=100
MCS=10
OUTPUT_FILE="/home/pi/Desktop/MCS_SWEEP_POWER/MCS_$MCS_$(date +%d_%H%M).log"

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


run_pw_config() {
    cd ~/nrc_pkg/script/
    echo -e "\n Setting TX PW to $1 dBm" | tee -a "$OUTPUT_FILE"
    ./cli_app set txpwr "$1" | tee -a "$OUTPUT_FILE"
    cd ~/Desktop
}

run_mcs_config() {
    cd ~/nrc_pkg/script/
    echo -e "\n Setting MCS to $1..." | tee -a "$OUTPUT_FILE"
    ./cli_app set config 0 0 "$1" | tee -a "$OUTPUT_FILE"
    cd ~/Desktop
}

# Main Function
main() {
    run_mcs_config "$MCS"
    echo "Starting Network Test Collection..." | tee -a $OUTPUT_FILE
    echo "Timestamp: $(date)" | tee -a $OUTPUT_FILE
    echo "iperf3 Server IP: $SERVER_IP" | tee -a $OUTPUT_FILE
    echo "iperf3 Test Duration: $IPERF3_DURATION seconds" | tee -a $OUTPUT_FILE
    echo "Ping Packet Count: $PING_COUNT" | tee -a $OUTPUT_FILE
 
    
    for ((i = 1; i < 21; i+=3)) 
    do
        echo -e "\n===================== PW $i =======================" | tee -a $OUTPUT_FILE 
	run_pw_config "$i"
	run_iperf3_test
	run_ping_test
	run_cli_test
	echo -e "\n================= DONE PW $i ======================" | tee -a $OUTPUT_FILE 
    done

    echo -e "\nNetwork test collection completed." | tee -a $OUTPUT_FILE
    echo "Results saved to $OUTPUT_FILE."
}

# Run the main function
main
