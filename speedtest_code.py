import csv
import speedtest
import time
from datetime import datetime

# Function to perform a speed test and return the results
def perform_speed_test():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    ping = st.results.ping  # Ping in milliseconds
    return download_speed, upload_speed, ping

# Function to record the speed test results in a CSV file
def record_speed_test_results(filename, download_speed, upload_speed, ping):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_time, download_speed, upload_speed, ping])
        return current_time

# Main function to schedule and record speed tests
# def main(interval_minutes, num_tests):
def main(interval_seconds, num_tests):
    # filename = 'speed_test_results.csv'
    filename = 'speed_test_results_PNPh-3rd_LAN.csv'
    
    # Create or append to the CSV file with headers if it doesn't exist
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(['Timestamp', 'Download Speed (Mbps)', 'Upload Speed (Mbps)', 'Ping (ms)'])

    for _ in range(num_tests):
        download_speed, upload_speed, ping = perform_speed_test()
        # record_speed_test_results(filename, download_speed, upload_speed, ping)
        current_time = record_speed_test_results(filename, download_speed, upload_speed, ping)
        # print(f'Test {_+1}: Download Speed: {download_speed:.2f} Mbps, Upload Speed: {upload_speed:.2f} Mbps, Ping: {ping} ms')
        print(f'Test {_+1}: Timestamp: {current_time}: Download Speed: {download_speed:.2f} Mbps, Upload Speed: {upload_speed:.2f} Mbps, Ping: {ping} ms')
        # time.sleep(interval_minutes * 60)
        time.sleep(interval_seconds)

if __name__ == "__main__":
    # interval_minutes = 1  # Adjust the interval (in minutes) between tests. Default is 30
    interval_seconds = 60  # Adjust the interval (in minutes) between tests. Default is 30
    num_tests = 540  # Approximately 9 hours. Adjust the number of tests to perform in a day. Default is 24
    # main(interval_minutes, num_tests)
    main(interval_seconds, num_tests)