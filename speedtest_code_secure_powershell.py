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
    try:
        os.system('speedtest --secure > results.txt')             # Automate speedtest at CMD and store the outputs

    except Exception as connection_error:
        print(f'{connection_error}')
        time.sleep(5)
        print("Restart speedtest")
        perform_speed_test(filename, interval_seconds)

    else:
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
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")                  # Capture time after speedtest execution

            # Print the output in the terminal
            # Need to implement try-catch for cases where target_isp is undefined
            # print(f'Time: {current_time}, Source: {source_isp} ({source_ip}), Target: {target_isp} - {target_km} km, Ping: {ping_ms} ms, Download: {download_speed} Mbps, Upload: {upload_speed} Mbps')

            print("")
            print(f'Timestamp: {time_at_request}')
            print(f'Client ISP: {source_isp} ({source_ip})')
            print(f'Remote ISP: {target_isp} - {target_km:.2f} km)')
            print(f'Ping: {ping_ms:.2f} ms, Download: {download_speed:.2f} Mbps, Upload: {upload_speed:.2f} Mbps')
            print("")
        
            t1 = datetime.strptime(time_at_request[11:], "%H:%M:%S")            # Format time to strptime formats
            t2 = datetime.strptime(current_time[11:], "%H:%M:%S")               # Format time to strptime formats
            delta = t2 - t1                                                     # Get the difference between time stamps
            adjusted_interval_seconds = datetime.strptime(str(interval_seconds), "%S") - delta  # Adjust delay of succeeding speedtest execution

            # Execute recording of the data to the CSV file
            record_speed_test_results(filename, current_time, source_isp, source_ip, target_isp, target_km, ping_ms, download_speed, upload_speed)

            time.sleep(int(adjusted_interval_seconds.strftime("%S")))   # Apply the adjusted time delay for next speedtest execution

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
    filename = 'speed_test_results_PNPh-3rd_Wifi.csv'
    interval_seconds = 30 # minumum of 30 seconds
    # num_tests = 2400 # Approvimately 20 hours
    num_tests = "unlimited"
    main(filename, interval_seconds, num_tests) # Calling the main method

'''
1 min   =  2 tests
1 hour  =  120 tests
5 hours =  600 tests
'''
