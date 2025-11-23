"""
Network information module - provides detailed network interface, connection, and routing info.
"""

import psutil
from sysx.utils.formatters import (
    print_header, print_subheader, print_key_value, 
    print_table, format_bytes
)
from sysx.utils.helpers import run_command, read_file_lines

def show_network_info():
    """Display comprehensive network information."""
    print_header("NETWORK INFORMATION")
    
    # Network Interfaces
    print_subheader("Network Interfaces")
    
    interfaces = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    
    interface_data = []
    
    for interface_name, addresses in interfaces.items():
        # Get interface status
        is_up = "up" if stats.get(interface_name) and stats[interface_name].isup else "down"
        
        # Get IP addresses
        ipv4 = "-"
        ipv6 = "-"
        mac = "-"
        
        for addr in addresses:
            if addr.family == 2:  # AF_INET (IPv4)
                ipv4 = addr.address
            elif addr.family == 10:  # AF_INET6 (IPv6)
                ipv6 = addr.address.split('%')[0]  # Remove scope ID
            elif addr.family == 17:  # AF_LINK (MAC)
                mac = addr.address
        
        interface_data.append([interface_name, is_up, ipv4, mac])
    
    if interface_data:
        headers = ["Interface", "Status", "IP Address", "MAC Address"]
        print_table(headers, interface_data)
    
    # Network Statistics
    print_subheader("Network Statistics")
    
    net_io = psutil.net_io_counters()
    print_key_value("Bytes Sent", format_bytes(net_io.bytes_sent))
    print_key_value("Bytes Received", format_bytes(net_io.bytes_recv))
    print_key_value("Packets Sent", str(net_io.packets_sent))
    print_key_value("Packets Received", str(net_io.packets_recv))
    print_key_value("Errors In", str(net_io.errin))
    print_key_value("Errors Out", str(net_io.errout))
    print_key_value("Dropped In", str(net_io.dropin))
    print_key_value("Dropped Out", str(net_io.dropout))
    
    # Per-Interface Statistics
    print_subheader("Per-Interface Statistics")
    
    per_interface = psutil.net_io_counters(pernic=True)
    interface_stats = []
    
    for interface, counters in per_interface.items():
        interface_stats.append([
            interface,
            format_bytes(counters.bytes_sent),
            format_bytes(counters.bytes_recv),
            str(counters.packets_sent),
            str(counters.packets_recv)
        ])
    
    if interface_stats:
        headers = ["Interface", "Sent", "Received", "Pkts Sent", "Pkts Recv"]
        print_table(headers, interface_stats)
    
    # Active Connections
    print_subheader("Active Network Connections")
    
    try:
        connections = psutil.net_connections(kind='inet')
        conn_data = []
        
        # Limit to first 20 connections
        for conn in connections[:20]:
            laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "-"
            raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "-"
            status = conn.status if conn.status else "-"
            
            conn_data.append([
                conn.type.name if hasattr(conn.type, 'name') else str(conn.type),
                laddr,
                raddr,
                status
            ])
        
        if conn_data:
            headers = ["Type", "Local Address", "Remote Address", "Status"]
            print_table(headers, conn_data)
            if len(connections) > 20:
                print(f"\n... and {len(connections) - 20} more connections")
        else:
            print("No active connections")
    except (PermissionError, psutil.AccessDenied):
        print("Permission denied - run with sudo for connection details")
    
    # Routing Table
    print_subheader("Routing Table")
    
    route_output = run_command("ip route")
    if route_output:
        route_lines = route_output.split('\n')
        print("\nRoutes:")
        for line in route_lines:
            if line.strip():
                print(f"  {line}")
    else:
        # Try netstat as fallback
        route_output = run_command("netstat -rn")
        if route_output:
            print("\n" + route_output)
    
    # DNS Configuration
    print_subheader("DNS Configuration")
    
    resolv_lines = read_file_lines("/etc/resolv.conf")
    if resolv_lines:
        nameservers = []
        for line in resolv_lines:
            if line.startswith("nameserver"):
                parts = line.split()
                if len(parts) >= 2:
                    nameservers.append(parts[1])
        
        if nameservers:
            for i, ns in enumerate(nameservers, 1):
                print_key_value(f"Nameserver {i}", ns)
    
    # Gateway Information
    gateways = psutil.net_if_addrs()
    default_gw = run_command("ip route | grep default")
    if default_gw:
        print_key_value("Default Gateway", default_gw.split()[2] if len(default_gw.split()) > 2 else "Unknown")
    
    print()  # Empty line at end
