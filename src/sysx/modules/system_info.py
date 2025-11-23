"""
System information module - provides detailed CPU, memory, disk, and hardware info.
"""

import psutil
import platform
from sysx.utils.formatters import (
    print_header, print_subheader, print_key_value, 
    print_table, format_bytes, format_percentage, format_uptime
)
from sysx.utils.helpers import (
    run_command, read_file, get_hostname, get_kernel_version, get_os_info
)

def show_system_info():
    """Display comprehensive system information."""
    print_header("SYSTEM INFORMATION")
    
    # Basic System Info
    print_subheader("System Overview")
    print_key_value("Hostname", get_hostname())
    print_key_value("Operating System", get_os_info())
    print_key_value("Kernel", get_kernel_version())
    print_key_value("Architecture", platform.machine())
    
    # Uptime
    try:
        uptime_seconds = psutil.boot_time()
        import time
        uptime = time.time() - uptime_seconds
        print_key_value("Uptime", format_uptime(uptime))
    except:
        pass
    
    # CPU Information
    print_subheader("CPU Information")
    
    # CPU model
    cpu_model = read_file("/proc/cpuinfo")
    if cpu_model:
        for line in cpu_model.split('\n'):
            if 'model name' in line:
                model = line.split(':')[1].strip()
                print_key_value("Model", model)
                break
    
    print_key_value("Physical Cores", str(psutil.cpu_count(logical=False)))
    print_key_value("Logical Cores", str(psutil.cpu_count(logical=True)))
    print_key_value("Architecture", platform.processor() or platform.machine())
    
    # CPU frequencies
    try:
        freq = psutil.cpu_freq()
        if freq:
            print_key_value("Current Speed", f"{freq.current:.0f} MHz")
            print_key_value("Min Speed", f"{freq.min:.0f} MHz")
            print_key_value("Max Speed", f"{freq.max:.0f} MHz")
    except:
        pass
    
    # CPU usage per core
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    print_key_value("CPU Usage (Overall)", f"{psutil.cpu_percent(interval=0)}%")
    
    # 🔥 NEW BLOCK: CPU + thermal sensor temperature readings
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                for entry in entries:
                    label = entry.label if entry.label else name
                    if entry.current:
                        print_key_value(f"Temperature ({label})", f"{entry.current}°C")
    except Exception:
        pass

    # Memory Information
    print_subheader("Memory Information")
    mem = psutil.virtual_memory()
    print_key_value("Total", format_bytes(mem.total))
    print_key_value("Available", format_bytes(mem.available))
    print_key_value("Used", format_bytes(mem.used))
    print_key_value("Free", format_bytes(mem.free))
    print_key_value("Usage", format_percentage(mem.used, mem.total))
    
    # Swap Memory
    swap = psutil.swap_memory()
    print_key_value("Swap Total", format_bytes(swap.total))
    print_key_value("Swap Used", format_bytes(swap.used))
    print_key_value("Swap Free", format_bytes(swap.free))
    print_key_value("Swap Usage", format_percentage(swap.used, swap.total))
    
    # Disk Information
    print_subheader("Disk Information")
    
    partitions = psutil.disk_partitions()
    disk_data = []
    
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_data.append([
                partition.device,
                partition.mountpoint,
                partition.fstype,
                format_bytes(usage.total),
                format_bytes(usage.used),
                format_bytes(usage.free),
                format_percentage(usage.used, usage.total)
            ])
        except PermissionError:
            continue
    
    if disk_data:
        headers = ["Device", "Mount Point", "FS Type", "Total", "Used", "Free", "Usage"]
        print_table(headers, disk_data)
    
    # Disk I/O Statistics
    try:
        disk_io = psutil.disk_io_counters()
        if disk_io:
            print_subheader("Disk I/O Statistics")
            print_key_value("Read Count", str(disk_io.read_count))
            print_key_value("Write Count", str(disk_io.write_count))
            print_key_value("Bytes Read", format_bytes(disk_io.read_bytes))
            print_key_value("Bytes Written", format_bytes(disk_io.write_bytes))
    except:
        pass
    
    # Hardware Information
    print_subheader("Hardware Information")
    
    # PCI Devices
    pci_output = run_command("lspci")
    if pci_output:
        pci_lines = pci_output.split('\n')[:10]  # Show first 10
        print("\nPCI Devices (first 10):")
        for line in pci_lines:
            print(f"  {line}")
    
    # USB Devices
    usb_output = run_command("lsusb")
    if usb_output:
        usb_lines = usb_output.split('\n')
        print("\nUSB Devices:")
        for line in usb_lines:
            if line.strip():
                print(f"  {line}")
    
    print()  # Empty line at end

