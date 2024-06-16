#!/usr/bin/expect -f

# Variables
set n 12

# Set timeout in seconds for commands
set timeout $n

cd ~/nrc_pkg/script
# Spawn the CLI application
spawn ./cli_app

# Expect the prompt
expect "NRC>"

# send "show config \r"

# Send the command and expect the output
send "show signal start 1 $n\r"
expect "OK"
expect "NRC>"
expect "NRC>"
set output $expect_out(buffer)

# Output the result without the prompt
puts [string trim $output]


# Exit
send "exit\r"
expect eof
