"""
Security check module - provides security auditing, firewall status, and port information.
"""

import psutil
import os
from sysx.utils.formatters import (
    print_header, print_subheader, print_key_value, print_table
)
from sysx.utils.helpers import run_command, read_file_lines, is_root, file_exists

def show_security_info():
    """Display comprehensive security information."""
    print_header("SECURITY STATUS")
    
    if not is_root():
        print("\nWARNING: Running without root privileges - some information may be limited")
        print("Run with sudo for complete security audit\n")
    
    # Firewall Status
    print_subheader("Firewall Status")
    
    # Check UFW
    ufw_status = run_command("ufw status")
    if ufw_status:
        print("\nUFW Firewall:")
        lines = ufw_status.split('\n')
        for line in lines[:10]:  # Show first 10 lines
            print(f"  {line}")
    else:
        # Check iptables
        iptables_output = run_command("iptables -L -n")
        if iptables_output:
            print("\niptables Rules (summary):")
            lines = iptables_output.split('\n')
            for line in lines[:15]:  # Show first 15 lines
                print(f"  {line}")
        else:
            print("Unable to determine firewall status")
    
    # Open Ports
    print_subheader("Open Ports (Listening)")
    
    try:
        connections = psutil.net_connections(kind='inet')
        listening_ports = []
        
        for conn in connections:
            if conn.status == 'LISTEN':
                port = conn.laddr.port if conn.laddr else None
                if port:
                    # Get process info
                    try:
                        proc = psutil.Process(conn.pid) if conn.pid else None
                        proc_name = proc.name() if proc else "-"
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        proc_name = "-"
                    
                    proto = "tcp" if conn.type == 1 else "udp"
                    addr = conn.laddr.ip if conn.laddr else "*"
                    
                    listening_ports.append([
                        str(port),
                        proto,
                        addr,
                        proc_name,
                        str(conn.pid) if conn.pid else "-"
                    ])
        
        # Remove duplicates and sort
        listening_ports = list(set(tuple(x) for x in listening_ports))
        listening_ports.sort(key=lambda x: int(x[0]))
        
        if listening_ports:
            headers = ["Port", "Protocol", "Address", "Process", "PID"]
            print_table(headers, [list(x) for x in listening_ports])
        else:
            print("No listening ports detected")
    except (PermissionError, psutil.AccessDenied):
        print("Permission denied - run with sudo to see open ports")
    
    # Failed Login Attempts
    print_subheader("Failed Login Attempts (Recent)")
    
    auth_log_paths = ['/var/log/auth.log', '/var/log/secure']
    failed_logins = []
    
    for log_path in auth_log_paths:
        if file_exists(log_path):
            try:
                lines = read_file_lines(log_path)
                for line in lines[-100:]:  # Check last 100 lines
                    if 'Failed password' in line or 'authentication failure' in line:
                        failed_logins.append(line)
            except PermissionError:
                print(f"Permission denied reading {log_path}")
                break
    
    if failed_logins:
        print(f"\nFound {len(failed_logins)} failed login attempts in logs:")
        for line in failed_logins[-10:]:  # Show last 10
            print(f"  {line[:100]}")  # Truncate long lines
        if len(failed_logins) > 10:
            print(f"  ... and {len(failed_logins) - 10} more")
    else:
        print("No recent failed login attempts found")
    
    # Running Services
    print_subheader("Running Services")
    
    systemctl_output = run_command("systemctl list-units --type=service --state=running --no-pager")
    if systemctl_output:
        lines = systemctl_output.split('\n')
        service_data = []
        
        for line in lines:
            if '.service' in line:
                parts = line.split()
                if len(parts) >= 4:
                    service_name = parts[0].replace('.service', '')
                    status = parts[2] if len(parts) > 2 else "-"
                    service_data.append([service_name, status])
        
        if service_data:
            headers = ["Service", "Status"]
            # Show first 20 services
            print_table(headers, service_data[:20])
            if len(service_data) > 20:
                print(f"\n... and {len(service_data) - 20} more services")
    else:
        print("Unable to list running services")
    
    # User Accounts
    print_subheader("User Accounts")
    
    passwd_lines = read_file_lines("/etc/passwd")
    if passwd_lines:
        user_data = []
        for line in passwd_lines:
            if line and not line.startswith('#'):
                parts = line.split(':')
                if len(parts) >= 7:
                    username = parts[0]
                    uid = parts[2]
                    shell = parts[6]
                    # Only show users with UID >= 1000 (regular users) or root
                    if uid == '0' or (uid.isdigit() and int(uid) >= 1000):
                        user_data.append([username, uid, shell])
        
        if user_data:
            headers = ["Username", "UID", "Shell"]
            print_table(headers, user_data)
    
    # SSH Configuration
    print_subheader("SSH Configuration")
    
    sshd_config = "/etc/ssh/sshd_config"
    if file_exists(sshd_config):
        config_lines = read_file_lines(sshd_config)
        important_settings = {
            'PermitRootLogin': 'Not set',
            'PasswordAuthentication': 'Not set',
            'Port': '22'
        }
        
        for line in config_lines:
            line = line.strip()
            if line and not line.startswith('#'):
                for key in important_settings.keys():
                    if line.startswith(key):
                        parts = line.split()
                        if len(parts) >= 2:
                            important_settings[key] = parts[1]
        
        for key, value in important_settings.items():
            print_key_value(key, value)
    else:
        print("SSH configuration not found")
    
    # SELinux / AppArmor Status
    print_subheader("Security Modules")
    
    selinux_status = run_command("getenforce")
    if selinux_status:
        print_key_value("SELinux Status", selinux_status)
    
    apparmor_status = run_command("aa-status")
    if apparmor_status:
        lines = apparmor_status.split('\n')
        print("\nAppArmor Status:")
        for line in lines[:5]:
            print(f"  {line}")
    
    print()  # Empty line at end
