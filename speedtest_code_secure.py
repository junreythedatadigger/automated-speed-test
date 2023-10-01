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
    time_at_request = datetime.now().strftime("%Y-%m-%d %H:%M:%S")      # Capture time before speedtest execution
    os.system('cmd /c "speedtest --secure > results.txt" ')             # Automate speedtest at CMD and store the outputs
    with open('results.txt') as f:                                      # Read the file containing the detailed speedtest results
        for index, line in enumerate(f):                                             # Get each line of characters and provide index
            if index == 1:
                source_isp = line[13:-4].split()[0]                                  # Get the source ISP
                source_ip = line[13:-4].split()[1][1:-1]                             # Get the source IP address
            elif index == 4:
                target_isp = line.split(":")[0][10:].split("[")[0][:-1]              # Get the targer ISP
                target_km =  float(line.split(":")[0][10:].split("[")[1][:-4])       # Get the target distance in km
                ping_ms = float(line.split(":")[1][1:-4])                            # Get the _ms in ms
            elif index == 6:
                download_speed = float(line.split()[1])                              # Get the download speed in Mbps
            elif index == 8:
                upload_speed = float(line.split()[1])                                # Get the upload speed in Mbps
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")                  # Capture time after speedtest execution

        # Print the output in the terminal
        print(f'Time: {current_time}, Source: {source_isp} ({source_ip}), Target: {target_isp} - {target_km} km, Download: {download_speed} Mbps, Upload: {upload_speed} Mbps, Ping: {ping_ms} ms')
        
        t1 = datetime.strptime(time_at_request[11:], "%H:%M:%S")            # Format time to strptime formats
        t2 = datetime.strptime(current_time[11:], "%H:%M:%S")               # Format time to strptime formats
        delta = t2 - t1                                                     # Get the difference between time stamps
        adjusted_interval_seconds = datetime.strptime(str(interval_seconds), "%S") - delta  # Adjust delay of succeeding speedtest execution

        # Execute recording of the data to the CSV file
        record_speed_test_results(filename, current_time, source_isp, source_ip, target_isp, target_km, download_speed, upload_speed, ping_ms)

        time.sleep(int(adjusted_interval_seconds.strftime("%S")))   # Apply the adjusted time delay for next speedtest execution

# The function to insert the speedtest results to the CSV file
def record_speed_test_results(filename, current_time, source_isp, source_ip, target_isp, target_km, download_speed, upload_speed, ping_ms):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_time, source_isp, source_ip, target_isp, target_km, download_speed, upload_speed, ping_ms])

# The main method to call the other methods
def main(filename, interval_seconds, num_tests):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(['Timestamp', 'Source ISP', 'Source IP', 'Target ISP', 'Target Distance (km)', 'Download Speed (Mbps)', 'Upload Speed (Mbps)' ,'Ping (ms)'])
    for _ in range(num_tests):
        perform_speed_test(filename, interval_seconds)


if __name__ == "__main__":
    filename = 'speed_test_results_Converge2.4G.csv'
    interval_seconds = 30 # minumum of 30 seconds
    num_tests = 600 # Approvimately 5 hours
    main(filename, interval_seconds, num_tests) # Calling the main method

'''
1 min   =  2 tests
1 hour  =  120 tests
5 hours =  600 tests
'''
