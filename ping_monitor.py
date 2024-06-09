import subprocess
import sys
import importlib
import pandas as pd
import time
from datetime import datetime
import matplotlib.pyplot as plt
import argparse
import numpy as np

# Function to install required packages
def install_packages():
    packages = ['pandas', 'matplotlib', 'argparse']
    for package in packages:
        try:
            importlib.import_module(package)
        except ImportError:
            print(f"Installing package: {package}")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# Call the function to install required packages
install_packages()

def ping(host, count=4, timeout=4):
    """
    Pings a host and returns the result.
    """
    result = subprocess.run(
        ["ping", "-c", str(count), "-W", str(timeout), host],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.stdout.decode(), result.stderr.decode()

def log_ping_results(host, interval, duration):
    """
    Logs ping results for the specified duration and interval.
    """
    end_time = time.time() + duration
    results = []

    while time.time() < end_time:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        stdout, stderr = ping(host)
        rtt = extract_rtt(stdout, stderr)
        result = {
            "timestamp": timestamp,
            "stdout": stdout,
            "stderr": stderr,
            "rtt": rtt
        }
        results.append(result)
        time.sleep(interval)

    return results

def extract_rtt(stdout, stderr):
    """
    Extracts the round-trip time from the ping output.
    """
    if 'Destination Host Unreachable' in stdout or stderr:
        return -1

    try:
        lines = stdout.split('\n')
        rtts = []
        for line in lines:
            if 'time=' in line:
                rtt = float(line.split('time=')[-1].split()[0])
                rtts.append(rtt)
        if rtts:
            return sum(rtts) / len(rtts)  # Return average RTT for the ping count
    except Exception as e:
        print(f"Error extracting RTT: {e}")
        return -1

    return -1

def save_results_to_csv(results, filename):
    """
    Saves the ping results to a CSV file.
    """
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)

def plot_ping_results(csv_file, plot_file, pie_file, title):
    df = pd.read_csv(csv_file)
    
    # Convert timestamp to datetime for proper plotting
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    plt.figure(figsize=(10, 5))
    plt.plot(df['timestamp'], df['rtt'], marker='o', linestyle='-', label='RTT')
    
    # Mark failed pings
    failed_pings = df[df['rtt'] == -1]
    plt.plot(failed_pings['timestamp'], failed_pings['rtt'], 'ro', label='Failed Ping')

    plt.xlabel('Time')
    plt.ylabel('Round-Trip Time (ms)')
    plt.title(title)
    plt.ylim(bottom=-2)
    plt.grid(True)
    plt.legend()
    plt.savefig(plot_file)
    #plt.show()

    # Pie chart for uptime
    online_count = df[df['rtt'] != -1].shape[0]
    offline_count = df[df['rtt'] == -1].shape[0]

    plt.figure(figsize=(6, 6))
    plt.pie(
        [online_count, offline_count],
        labels=['Online', 'Offline'],
        autopct='%1.1f%%',
        colors=['#4CAF50', '#FF5252']
    )
    plt.title(f'Uptime for {title}')
    plt.savefig(pie_file)
    #plt.show()

def main():
    parser = argparse.ArgumentParser(description="Ping Monitoring Script")
    parser.add_argument('--host', type=str, required=True, help='The host to ping')
    parser.add_argument('--interval', type=int, default=60, help='Ping interval in seconds')
    parser.add_argument('--duration', type=int, default=3600, help='Total duration in seconds')

    args = parser.parse_args()

    host = args.host
    interval = args.interval
    duration = args.duration

    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_filename = f"{host}_{current_time}_ping_results.csv"
    plot_filename = f"{host}_{current_time}_ping_results_plot.jpg"
    pie_filename = f"{host}_{current_time}_ping_results_pie.jpg"
    plot_title = f"Ping Results for {host} at {current_time}"

    print(f"Starting to ping {host} every {interval} seconds for {duration // 60} minutes.")
    results = log_ping_results(host, interval, duration)
    save_results_to_csv(results, csv_filename)
    print(f"Results saved to {csv_filename}")

    plot_ping_results(csv_filename, plot_filename, pie_filename, plot_title)
    print(f"Plots saved to {plot_filename} and {pie_filename}")

if __name__ == "__main__":
    main()
