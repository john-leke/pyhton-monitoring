#!/usr/bin/env python3

import csv
import os
from extract_metrics import extract_metrics
import time

# CSV file location
CSV_FILE = 'system_metrics.csv'

def save_metrics_to_csv(data):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            # Create the header row if the file doesn't exist
            writer.writerow(['Timestamp', 'Hostname', 'Network Interfaces', 'CPU Usage (%)', 'CPU Frequency (MHz)',
                             'CPU Cores', 'Memory Total (GB)', 'Memory Usage (%)', 'Disk Usage (%)', 'Uptime (seconds)', 'Load Average (1 min)'])
        
        # Write the data row
        writer.writerow(data)

def collect_and_store_metrics():
    metrics = extract_metrics()

    # Prepare data for CSV entry
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    network_info = str(metrics['network_interfaces'])
    csv_data = [timestamp, metrics['hostname'], network_info, metrics['cpu_usage'], metrics['cpu_frequency'],
                metrics['cpu_cores'], metrics['memory_total'], metrics['memory_usage'],
                str(metrics['disk_usage']), metrics['uptime'], metrics['load_average']]

    # Save to CSV
    save_metrics_to_csv(csv_data)

if __name__ == "__main__":
    # Periodically collect and store metrics
    while True:
        collect_and_store_metrics()
        time.sleep(10)
