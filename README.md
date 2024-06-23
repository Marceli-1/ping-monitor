# Ping Monitoring Script

This script pings a specified host at regular intervals over a specified duration and logs the results. It generates a plot of the round-trip times (RTTs) over time and a pie chart showing the uptime (online vs. offline). The script also includes functionality to automatically install required packages if they are not already installed.

## Features

- Logs ping results to a CSV file.
- Generates a plot of RTTs over time.
- Creates a pie chart showing uptime (online vs. offline).
- Command-line interface for specifying host, interval, and duration.
- Automatically installs required packages.

## Requirements

- Python 3.x

## Usage

1. **Clone the repository:**
```
git clone https://github.com/Marceli-1/ping-monitor.git
cd ping-monitoring
```

2. Run the script:
```
python ping_monitor.py --host <host> --interval <interval> --duration <duration>
```

## Example:
```
python ping_monitor.py --host 8.8.8.8 --interval 60 --duration 3600
```

This will start pinging 8.8.8.8 every 60 seconds for 1 hour, save the results to a dynamically named CSV file, and generate both a plot of the RTT over time and a pie chart showing the uptime.

Script Description
The script consists of the following functions:

install_packages(): Installs the required Python packages if they are not already installed.
ping(host, count=4, timeout=4): Pings the specified host and returns the result.
log_ping_results(host, interval, duration): Logs the ping results at the specified interval for the specified duration.
extract_rtt(stdout, stderr): Extracts the round-trip time from the ping output.
save_results_to_csv(results, filename): Saves the ping results to a CSV file.
plot_ping_results(csv_file, plot_file, pie_file, title): Generates a plot of RTTs over time and a pie chart showing uptime.
Example Output

### The script generates following files:

CSV File: <host>_<timestamp>_ping_results.csv - Contains the logged ping results.

### Plots:

<host>_<timestamp>_ping_results_plot.jpg - A plot of RTTs over time.
<host>_<timestamp>_ping_results_pie.jpg - A pie chart showing uptime (online vs. offline).
