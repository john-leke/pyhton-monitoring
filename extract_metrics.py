#!/usr/bin/env python3

import psutil
import socket
import datetime
import os
import pytz
import platform
from time import time

def extract_metrics():
    # Get the system hostname
    hostname = socket.gethostname()

    # Collect information about network interfaces and IP addresses
    net_if_addrs = psutil.net_if_addrs()
    network_interfaces = {}
    for interface_name, interface_addrs in net_if_addrs.items():
        ips = [addr.address for addr in interface_addrs if addr.family == socket.AF_INET]
        network_interfaces[interface_name] = ips

    # Get current system time along with timezone
    current_time = datetime.datetime.now()
    timezone = datetime.datetime.now(pytz.timezone('UTC')).astimezone().tzname()

    # Detect OS type
    os_type = platform.system()

    # CPU stats: usage and frequency
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else None
    cpu_cores = psutil.cpu_count(logical=False)

    # Memory stats: total and usage percentage
    memory = psutil.virtual_memory()
    total_memory = memory.total / (1024 * 1024 * 1024)  # Convert to GB
    memory_usage = memory.percent

    # Disk stats: total capacity and usage
    disks = psutil.disk_partitions()
    disk_usage_info = {}
    for disk in disks:
        if 'rw' in disk.opts:
            usage = psutil.disk_usage(disk.mountpoint)
            disk_usage_info[disk.device] = {
                'total': usage.total / (1024 * 1024 * 1024),  # Convert to GB
                'used': usage.percent
            }

    # Uptime and system load
    uptime_seconds = time() - psutil.boot_time()
    load_avg = os.getloadavg()[0] if os_type != 'Windows' else None

    # Combine all metrics into a dictionary
    metrics = {
        'hostname': hostname,
        'network_interfaces': network_interfaces,
        'current_time': current_time.strftime(f"%Y-%m-%d %H:%M:%S {timezone}"),
        'cpu_usage': cpu_usage,
        'cpu_frequency': cpu_freq,
        'cpu_cores': cpu_cores,
        'memory_total': total_memory,
        'memory_usage': memory_usage,
        'disk_usage': disk_usage_info,
        'uptime': uptime_seconds,
        'load_average': load_avg
    }

    return metrics

if __name__ == "__main__":
    metrics = extract_metrics()
    print(metrics)
