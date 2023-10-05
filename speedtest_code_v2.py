import csv
import speedtest
import time
from datetime import datetime
import pytz

# Function to perform a speed test and return the results
def perform_speed_test(interval_seconds):

    # Get the timestamp at the start of speedtest request
    time_at_request = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        st = speedtest.Speedtest()
        st._secure = True
        st.get_best_server() # Same as st._best

        # Store the result of getting the best server
        results = st.results
        
        # Get the raw date from the timestamp of results
        rawdate = results.timestamp.split("T")[0].split("-")

        # Get the raw time from the timestamp of results
        rawtime = results.timestamp.split("T")[1].split(":")

        # Format the timestamp to include the UTC timezone
        utc_timestamp = datetime(int(rawdate[0]), int(rawdate[1]), int(rawdate[2]), int(rawtime[0]), int(rawtime[1]), int(float(rawtime[2][:-3])), tzinfo=pytz.utc)

        # Convert UTC timestamp to Asia/Manila timestamp
        ph_timestamp = utc_timestamp.astimezone(pytz.timezone("Asia/Manila")).strftime('%Y-%m-%d %H:%M:%S')

        # Get the other details from the results
        remote_isp = results.server["sponsor"]          # Get the remote ISP name
        remote_isp_loc = results.server["name"]         # Get the remote ISP location
        remote_isp_dis = results.server["d"]            # Get the remote ISP distance
        # remote_isp_ping = results.server["latency"]     # Get the remote server latency. Same as ping value
        client_isp = results.client["isp"]              # Get the client ISP name
        client_isp_ip = results.client["ip"]            # Get the client ISP IP address

        # Get the download speed after the speed test
        download_speed = st.download() / 1_000_000  # Convert to Mbps

        # Get the upload spped after the speed test
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps

        # Get the latency of the ping test
        ping = st.results.ping  # Ping in milliseconds

        # Calculate the adjustment of interval between speedtest request
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")         # Get the timestamp after getting the results
        t1 = datetime.strptime(time_at_request[11:], "%H:%M:%S")            # Format time to strptime formats
        t2 = datetime.strptime(current_time[11:], "%H:%M:%S")               # Format time to strptime formats
        delta = t2 - t1                                                     # Get the difference between time stamps
        adjusted_interval = datetime.strptime(str(interval_seconds), "%S") - delta  # Adjust delay of succeeding speedtest execution
        adjusted_interval_seconds = int(adjusted_interval.strftime("%S"))   # Convert the datetime seconds to integer

        # Return the required values
        return ph_timestamp, client_isp, client_isp_ip, remote_isp, remote_isp_loc, remote_isp_dis, ping, download_speed, upload_speed, adjusted_interval_seconds
    except:
        print("error")
        time.sleep(5)
        perform_speed_test(interval_seconds)

# Function to record the speed test results in a CSV file
def record_speed_test_results(filename, ph_timestamp, client_isp, client_isp_ip, remote_isp, remote_isp_loc, remote_isp_dis, ping, download_speed, upload_speed):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ph_timestamp, client_isp, client_isp_ip, remote_isp, remote_isp_loc, round(remote_isp_dis, 2) , round(ping, 2), round(download_speed, 2), round(upload_speed, 2)])

# Main function to schedule and record speed tests
def main(interval_seconds, num_tests):
    # filename = 'speed_test_results.csv'
    # filename = 'speed_test_results_PNPh-3rd_LAN.csv'
    filename = 'speed_test_results_PNPh-3rd_Wifi_2023-10-05b.csv'
    
    # Create or append to the CSV file with headers if it doesn't exist
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(['Timestamp', 'Client', 'IP', 'Remote', 'Location', 'Distance (km)', 'Ping (ms)', 'Download Speed (Mbps)', 'Upload Speed (Mbps)'])

    for _ in range(num_tests):
        ph_timestamp, client_isp, client_isp_ip, remote_isp, remote_isp_loc, remote_isp_dis, ping, download_speed, upload_speed, adjusted_interval_seconds = perform_speed_test(interval_seconds)
        record_speed_test_results(filename, ph_timestamp, client_isp, client_isp_ip, remote_isp, remote_isp_loc, remote_isp_dis, ping, download_speed, upload_speed)

        print("")
        print(f'Timestamp: {ph_timestamp}')
        print(f'Client ISP: {client_isp} ({client_isp_ip})')
        print(f'Remote ISP: {remote_isp} ({remote_isp_loc} - {remote_isp_dis:.2f} km)')
        print(f'Ping: {ping:.2f} ms, Download: {download_speed:.2f} Mbps, Upload: {upload_speed:.2f} Mbps')
        print("")

        time.sleep(adjusted_interval_seconds)

if __name__ == "__main__":
    interval_seconds = 60  # Adjust the interval (in seconds) between tests. Minimum is 30
    num_tests = 1440        # Approximately 24 hours.
    main(interval_seconds, num_tests)