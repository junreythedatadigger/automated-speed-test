'''
Sources

https://www.tutorialspoint.com/command-line-automation-in-python
'''

import csv
# import speedtest
import time
from datetime import datetime
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Credential file path
absolute_path = os.path.dirname(__file__)                               # the current location of this project
relative_path = "data-analyst-project-01-384107-9457afc61153.json"      # relative path credential
full_path = os.path.join(absolute_path, relative_path)

# Google Sheets Settings
spreadsheet_id = "139-CU26KtY9eJ6H8Vm8Ygp89l7d7q9M7_GjrJ0noBZU"
credentials_file = full_path

# Connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
client = gspread.authorize(credentials)
sheet = client.open_by_key(spreadsheet_id).sheet1

index_last = 0

# The function to automate execution of speedtest in CMD
def perform_speed_test(filename, interval_seconds, index_last):
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
        record_speed_test_results(filename, pre_test_time_display, source_isp, source_ip, target_isp, target_km, ping_ms, download_speed, upload_speed, index_last)

        # Return the adjusted time delay for next speedtest execution
        time.sleep(adjusted_interval_seconds)

# The function to insert the speedtest results to the CSV file
def record_speed_test_results(filename, current_time, source_isp, source_ip, target_isp, target_km, ping_ms, download_speed, upload_speed, index_last):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_time, source_isp, source_ip, target_isp, target_km, ping_ms, download_speed, upload_speed])

    data_list = [current_time, source_isp, source_ip, target_isp, target_km, ping_ms, download_speed, upload_speed]

    cell_rows = sheet.range('A'+str(index_last)+':H'+str(index_last))

    index = 0

    for cell in cell_rows:
        cell.value = data_list[index]
        index += 1

    sheet.update_cells(cell_rows)

# The main method to call the other methods
def main(filename, interval_seconds, num_tests, index_last):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(['Timestamp', 'Source ISP', 'Source IP', 'Target ISP', 'Target Distance (km)' ,'Ping (ms)', 'Download Speed (Mbps)', 'Upload Speed (Mbps)'])

    if (num_tests == "unlimited"):
        while True:
            perform_speed_test(filename, interval_seconds, index_last)
            index_last += 1
    else:
        for _ in range(num_tests):
            perform_speed_test(filename, interval_seconds, index_last)
            index_last += 1


if __name__ == "__main__":
    # Get the last column with values then add 1
    index_last = len(sheet.col_values(1)) + 1

    filename = 'speed_test_results_Converge2.4G.csv'
    interval_seconds = 30 # minumum of 30 seconds
    # num_tests = 600 # Approvimately 5 hours
    num_tests = "unlimited"
    main(filename, interval_seconds, num_tests, index_last) # Calling the main method

'''
1 min   =  2 tests
1 hour  =  120 tests
5 hours =  600 tests
'''
