#!/usr/bin/env python3

from flask import Flask, Response
from prometheus_client import Gauge, generate_latest
from extract_metrics import extract_metrics
import platform

app = Flask(__name__)

# Prometheus metrics definition
cpu_usage_gauge = Gauge('cpu_usage_percent', 'Percentage of CPU usage')
cpu_freq_gauge = Gauge('cpu_frequency_mhz', 'Current CPU frequency in MHz')
cpu_cores_gauge = Gauge('cpu_cores', 'Physical CPU cores count')
memory_total_gauge = Gauge('memory_total_gb', 'Total system memory in GB')
memory_usage_gauge = Gauge('memory_usage_percent', 'Percentage of memory usage')
disk_usage_gauge = Gauge('disk_usage_percent', 'Disk usage for each partition')
uptime_gauge = Gauge('uptime_seconds', 'System uptime in seconds')
load_avg_gauge = Gauge('system_load_average', 'System load average over 1 minute')

def update_metrics():
    metrics = extract_metrics()
    
    cpu_usage_gauge.set(metrics['cpu_usage'])
    cpu_freq_gauge.set(metrics['cpu_frequency'] if metrics['cpu_frequency'] else 0)
    cpu_cores_gauge.set(metrics['cpu_cores'])
    memory_total_gauge.set(metrics['memory_total'])
    memory_usage_gauge.set(metrics['memory_usage'])

    for disk, usage in metrics['disk_usage'].items():
        disk_usage_gauge.labels(disk=disk).set(usage['used'])

    uptime_gauge.set(metrics['uptime'])
    if metrics['load_average'] is not None:
        load_avg_gauge.set(metrics['load_average'])

@app.route('/metrics')
def metrics():
    update_metrics()
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
