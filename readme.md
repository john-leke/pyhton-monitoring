Summary of Scripts:
Script 1 (extract_metrics.py):

Extracts all necessary metrics, including hostname, network interfaces, date and time, CPU stats, memory stats, disk usage, system uptime, and load averages.
Outputs the metrics as a dictionary that can be used by other scripts.
Script 2 (prometheus_metrics.py):

Uses Flask to expose a /metrics HTTP endpoint.
Converts the metrics into Prometheus-compatible format using the prometheus_client library.
Updates and serves the metrics whenever the /metrics endpoint is accessed.
Script 3 (save_metrics_to_csv.py):

Collects the metrics and writes them to a CSV file every 10 seconds.
Each row in the CSV includes a timestamp, metrics data, and a snapshot of the system's state.


sudo apt update
sudo apt install python3 python3-pip
sudo apt install pipx


#Installing Required Python Packages
pipx install psutil
pipx install flask
pipx install prometheus_client
pipx install pytz


Run the following command to make the script executable
chmod +x extract_metrics.py

Execute the script with
./extract_metrics.py

Run the following command to make the script executable
chmod +x prometheus_metrics.py

Execute the script with
./prometheus_metrics.py
