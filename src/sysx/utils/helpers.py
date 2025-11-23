"""
Helper utilities for running system commands and file operations.
"""

import subprocess
import os
import platform

def run_command(command, shell=False):
    """
    Execute a system command and return output.
    
    Args:
        command: Command to run (string or list)
        shell: Whether to use shell execution
    
    Returns:
        Command output as string, or None if error
    """
    try:
        if isinstance(command, str) and not shell:
            command = command.split()
        
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        return None

def read_file(filepath):
    """
    Safely read a text file.
    
    Args:
        filepath: Path to file
    
    Returns:
        File contents as string, or None if error
    """
    try:
        with open(filepath, 'r') as f:
            return f.read().strip()
    except (IOError, FileNotFoundError, PermissionError):
        return None

def read_file_lines(filepath):
    """
    Safely read a text file as lines.
    
    Args:
        filepath: Path to file
    
    Returns:
        List of lines, or empty list if error
    """
    try:
        with open(filepath, 'r') as f:
            return [line.strip() for line in f.readlines()]
    except (IOError, FileNotFoundError, PermissionError):
        return []

def file_exists(filepath):
    """Check if file exists."""
    return os.path.isfile(filepath)

def dir_exists(dirpath):
    """Check if directory exists."""
    return os.path.isdir(dirpath)

def get_dir_size(dirpath):
    """
    Calculate total size of directory.
    
    Args:
        dirpath: Path to directory
    
    Returns:
        Size in bytes
    """
    total_size = 0
    try:
        for dirpath_inner, dirnames, filenames in os.walk(dirpath):
            for filename in filenames:
                filepath = os.path.join(dirpath_inner, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, FileNotFoundError):
                    continue
    except (OSError, PermissionError):
        pass
    return total_size

def is_root():
    """Check if script is running with root privileges."""
    return os.geteuid() == 0 if hasattr(os, 'geteuid') else False

def get_hostname():
    """Get system hostname."""
    return platform.node()

def get_kernel_version():
    """Get kernel version."""
    return platform.release()

def get_os_info():
    """Get OS name and version."""
    try:
        with open('/etc/os-release') as f:
            lines = f.readlines()
            os_info = {}
            for line in lines:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    os_info[key] = value.strip('"')
            
            name = os_info.get('PRETTY_NAME', os_info.get('NAME', 'Unknown'))
            return name
    except (IOError, FileNotFoundError):
        return f"{platform.system()} {platform.release()}"

def command_exists(command):
    """Check if a command exists in PATH."""
    return run_command(f"which {command}") is not None
