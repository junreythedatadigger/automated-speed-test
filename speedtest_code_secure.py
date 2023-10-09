'''
Sources

https://www.tutorialspoint.com/command-line-automation-in-python
'''

import csv
# import speedtest
import time
from datetime import datetime

import os

# The function to automate execution of speedtest in CMD
def perform_speed_test(filename, interval_seconds):
    pre_test_time = datetime.now()                                          # Capture time before speedtest execution
    pre_test_time_display = pre_test_time.strftime("%Y-%m-%d %H:%M:%S")     # Format pre_test_time for display/storage
    pre_test_time_calculate = pre_test_time.timestamp()                     # Format pre_test_time for calculations
    
    os.system('cmd /c "speedtest --secure > results.txt" ')             # Automate speedtest at CMD and store the outputs

    with open('results.txt') as f:                                      # Read the file containing the detailed speedtest results
        for index, line in enumerate(f):                                             # Get each line of characters and provide index
            if index == 1:
                source_isp = line[13:-4].split("(")[0][:-1]                          # Get the source ISP
                source_ip = line[13:-4].split("(")[1][:-1]                           # Get the source IP address
            elif index == 4:
                target_isp = line.split(":")[0][10:].split("[")[0][:-1]              # Get the targer ISP
                target_km =  float(line.split(":")[0][10:].split("[")[1][:-4])       # Get the target distance in km
                ping_ms = float(line.split(":")[1][1:-4])                            # Get the _ms in ms
            elif index == 6:
                download_speed = float(line.split()[1])                              # Get the download speed in Mbps
            elif index == 8:
                upload_speed = float(line.split()[1])                                # Get the upload speed in Mbps

    post_test_time = datetime.now()                                         # Capture time after speedtest execution
    post_test_time_calculate = post_test_time.timestamp()                   # Format post_test_time for calculations


    # Print the output in the terminal
    try:
        target_isp                      # Check if target_isp was assigned a value

    except Exception as value_error:
        print(f'{value_error}')
        time.sleep(5)
        print("Restart speedtest execution")
        perform_speed_test(filename, interval_seconds)

    else:
        print("")
        print(f'Timestamp: {pre_test_time_display}')
        print(f'Client ISP: {source_isp} ({source_ip})')
        print(f'Remote ISP: {target_isp} - {target_km:.2f} km)')
        print(f'Ping: {ping_ms:.2f} ms, Download: {download_speed:.2f} Mbps, Upload: {upload_speed:.2f} Mbps')
        print("")

        # Adjust the interval between speedtest requests executions
        adjusted_interval_seconds = abs(int(interval_seconds - post_test_time_calculate + pre_test_time_calculate))

        # Execute recording of the data to the CSV file
        record_speed_test_results(filename, pre_test_time_display, source_isp, source_ip, target_isp, target_km, ping_ms, download_speed, upload_speed)

        # Return the adjusted time delay for next speedtest execution
        time.sleep(adjusted_interval_seconds)

# The function to insert the speedtest results to the CSV file
def record_speed_test_results(filename, current_time, source_isp, source_ip, target_isp, target_km, ping_ms, download_speed, upload_speed):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_time, source_isp, source_ip, target_isp, target_km, ping_ms, download_speed, upload_speed])

# The main method to call the other methods
def main(filename, interval_seconds, num_tests):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(['Timestamp', 'Source ISP', 'Source IP', 'Target ISP', 'Target Distance (km)' ,'Ping (ms)', 'Download Speed (Mbps)', 'Upload Speed (Mbps)'])

    if (num_tests == "unlimited"):
        while True:
            perform_speed_test(filename, interval_seconds)
    else:
        for _ in range(num_tests):
            perform_speed_test(filename, interval_seconds)


if __name__ == "__main__":
    filename = 'speed_test_results_Converge2.4G.csv'
    interval_seconds = 30 # minumum of 30 seconds
    # num_tests = 600 # Approvimately 5 hours
    num_tests = "unlimited"
    main(filename, interval_seconds, num_tests) # Calling the main method

'''
1 min   =  2 tests
1 hour  =  120 tests
5 hours =  600 tests
'''
