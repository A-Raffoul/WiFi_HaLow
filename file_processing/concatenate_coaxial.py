import os
import re

# Define the base directories for AP and STA logs
ap_base_dir = r'C:\Users\raffoul\Desktop\coaxial_rc_AP_characterization'
sta_base_dir = r'C:\Users\raffoul\Desktop\coaxial_rc_STA_characterization'
output_base_dir = r'C:\Users\raffoul\Desktop\WiFi_HaLow\data\coaxial'

# Create output base directory if it doesn't exist
os.makedirs(output_base_dir, exist_ok=True)

# Function to extract txpwr value from filename
def extract_txpwr(filename):
    match = re.search(r'txpwr(\d+)', filename)
    return int(match.group(1)) if match else None

# Function to get all relevant files from a directory
def get_log_files(directory):
    files = []
    pattern = re.compile(r'coaxial_txpwr\d+_\d+MHz_\d+dBm_(AP|STA)\.log', re.IGNORECASE)
    for file in os.listdir(directory):
        if pattern.match(file):
            files.append(file)
    return files

# Iterate through each subdirectory in the AP base directory
for ap_subdir in os.listdir(ap_base_dir):
    ap_subdir_path = os.path.join(ap_base_dir, ap_subdir)
    print(f'Processing {ap_subdir_path}...')
    if os.path.isdir(ap_subdir_path) and ap_subdir.startswith('results_'):
        # Derive the corresponding STA subdirectory
        sta_subdir = ap_subdir.replace('_AP_', '_STA_')
        sta_subdir_path = os.path.join(sta_base_dir, sta_subdir)
        print(f'Corresponding STA subdirectory: {sta_subdir_path}')
        
        # Check if the corresponding STA subdirectory exists
        if os.path.exists(sta_subdir_path):
            # Create the output directory for this pair
            output_dir = os.path.join(output_base_dir, sta_subdir)
            os.makedirs(output_dir, exist_ok=True)
            
            # Get all AP and STA log files
            ap_files = get_log_files(ap_subdir_path)
            sta_files = get_log_files(sta_subdir_path)
    
            print(f'AP subdir path: {ap_subdir_path}')
            print(f'STA subdir path: {sta_subdir_path}')
            print(f'AP files: {ap_files}')
            print(f'STA files: {sta_files}')
            
            # Organize files by txpwr value
            ap_logs = {extract_txpwr(file): file for file in ap_files}
            sta_logs = {extract_txpwr(file): file for file in sta_files}
            
            # Iterate over all possible txpwr values
            for txpwr in range(21):
                if txpwr in ap_logs and txpwr in sta_logs:
                    # Construct full paths to the files
                    ap_filepath = os.path.join(ap_subdir_path, ap_logs[txpwr])
                    sta_filepath = os.path.join(sta_subdir_path, sta_logs[txpwr])
                    
                    # Read the contents of the STA log
                    with open(sta_filepath, 'r') as sta_file:
                        sta_content = sta_file.read()
                    
                    # Read the contents of the AP log
                    with open(ap_filepath, 'r') as ap_file:
                        ap_content = ap_file.read()
                    
                    # Concatenate STA and AP contents (STA first, then AP)
                    concatenated_content = sta_content + "\n" + ap_content
                    
                    # Define the output filename and path
                    output_filename = ap_logs[txpwr].replace('_AP.log', '_combined.log')
                    output_filepath = os.path.join(output_dir, output_filename)
                    
                    # Write the concatenated content to the output file
                    with open(output_filepath, 'w') as output_file:
                        output_file.write(concatenated_content)
                    
                    print(f'Concatenated files for txpwr{txpwr} in {sta_subdir} and saved to {output_filepath}')
                else:
                    print(f'Skipping txpwr{txpwr} in {sta_subdir} as one or both files are missing.')

print('Concatenation process completed.')
