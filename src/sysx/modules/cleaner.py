"""
System cleaning module - removes cache, logs, temporary files, and package leftovers.
"""

import os
import subprocess
from sysx.utils.formatters import (
    print_header, print_subheader, print_key_value, format_bytes
)
from sysx.utils.helpers import (
    run_command, get_dir_size, dir_exists, is_root, command_exists
)

def scan_cleanable_items():
    """
    Scan system for cleanable items and return dictionary with sizes.
    
    Returns:
        Dictionary with category names and sizes in bytes
    """
    cleanable = {}
    
    # APT Cache (Debian/Ubuntu)
    apt_cache = "/var/cache/apt/archives"
    if dir_exists(apt_cache):
        cleanable['apt_cache'] = get_dir_size(apt_cache)
    
    # DNF/YUM Cache (Fedora/RHEL)
    dnf_cache = "/var/cache/dnf"
    yum_cache = "/var/cache/yum"
    if dir_exists(dnf_cache):
        cleanable['dnf_cache'] = get_dir_size(dnf_cache)
    elif dir_exists(yum_cache):
        cleanable['yum_cache'] = get_dir_size(yum_cache)
    
    # User Cache
    home = os.path.expanduser("~")
    user_cache = os.path.join(home, ".cache")
    if dir_exists(user_cache):
        cleanable['user_cache'] = get_dir_size(user_cache)
    
    # Thumbnail Cache
    thumbnail_cache = os.path.join(home, ".cache", "thumbnails")
    if dir_exists(thumbnail_cache):
        cleanable['thumbnail_cache'] = get_dir_size(thumbnail_cache)
    
    # Temporary Directories
    if dir_exists("/tmp"):
        cleanable['tmp'] = get_dir_size("/tmp")
    
    if dir_exists("/var/tmp"):
        cleanable['var_tmp'] = get_dir_size("/var/tmp")
    
    # System Logs
    if dir_exists("/var/log"):
        try:
            cleanable['system_logs'] = get_dir_size("/var/log")
        except PermissionError:
            cleanable['system_logs'] = 0
    
    # Journal Logs
    journal_dir = "/var/log/journal"
    if dir_exists(journal_dir):
        try:
            cleanable['journal_logs'] = get_dir_size(journal_dir)
        except PermissionError:
            cleanable['journal_logs'] = 0
    
    # Old log files (compressed)
    old_logs = 0
    if dir_exists("/var/log"):
        try:
            for root, dirs, files in os.walk("/var/log"):
                for file in files:
                    if file.endswith(('.gz', '.1', '.2', '.old')):
                        try:
                            old_logs += os.path.getsize(os.path.join(root, file))
                        except (OSError, PermissionError):
                            continue
        except PermissionError:
            pass
    cleanable['old_logs'] = old_logs
    
    return cleanable

def show_cleanable_summary(cleanable):
    """Display summary of cleanable items."""
    print_subheader("Cache")
    
    if 'apt_cache' in cleanable:
        print_key_value("APT Cache", format_bytes(cleanable['apt_cache']))
    
    if 'dnf_cache' in cleanable:
        print_key_value("DNF Cache", format_bytes(cleanable['dnf_cache']))
    
    if 'yum_cache' in cleanable:
        print_key_value("YUM Cache", format_bytes(cleanable['yum_cache']))
    
    if 'user_cache' in cleanable:
        print_key_value("User Cache", format_bytes(cleanable['user_cache']))
    
    if 'thumbnail_cache' in cleanable:
        print_key_value("Thumbnail Cache", format_bytes(cleanable['thumbnail_cache']))
    
    print_subheader("Logs")
    
    if 'system_logs' in cleanable:
        print_key_value("System Logs", format_bytes(cleanable['system_logs']))
    
    if 'journal_logs' in cleanable:
        print_key_value("Journal Logs", format_bytes(cleanable['journal_logs']))
    
    if 'old_logs' in cleanable:
        print_key_value("Old/Compressed Logs", format_bytes(cleanable['old_logs']))
    
    print_subheader("Temporary Files")
    
    if 'tmp' in cleanable:
        print_key_value("/tmp", format_bytes(cleanable['tmp']))
    
    if 'var_tmp' in cleanable:
        print_key_value("/var/tmp", format_bytes(cleanable['var_tmp']))

def clean_apt_cache():
    """Clean APT package cache."""
    if command_exists("apt-get"):
        print("Cleaning APT cache...")
        run_command("apt-get clean")
        run_command("apt-get autoclean")
        print("APT cache cleaned")

def clean_dnf_cache():
    """Clean DNF package cache."""
    if command_exists("dnf"):
        print("Cleaning DNF cache...")
        run_command("dnf clean all")
        print("DNF cache cleaned")

def clean_yum_cache():
    """Clean YUM package cache."""
    if command_exists("yum"):
        print("Cleaning YUM cache...")
        run_command("yum clean all")
        print("YUM cache cleaned")

def clean_user_cache():
    """Clean user cache directory."""
    home = os.path.expanduser("~")
    cache_dir = os.path.join(home, ".cache")
    
    if dir_exists(cache_dir):
        print("Cleaning user cache...")
        # Only remove safe subdirectories
        safe_dirs = ['thumbnails', 'mozilla', 'chromium', 'google-chrome']
        for subdir in safe_dirs:
            subdir_path = os.path.join(cache_dir, subdir)
            if dir_exists(subdir_path):
                try:
                    run_command(f"rm -rf {subdir_path}/*", shell=True)
                except:
                    pass
        print("User cache cleaned")

def clean_journal_logs():
    """Clean systemd journal logs."""
    if command_exists("journalctl"):
        print("Cleaning journal logs (keeping last 3 days)...")
        run_command("journalctl --vacuum-time=3d")
        print("Journal logs cleaned")

def clean_old_logs():
    """Remove old compressed log files."""
    if dir_exists("/var/log"):
        print("Removing old compressed logs...")
        run_command("find /var/log -type f -name '*.gz' -delete", shell=True)
        run_command("find /var/log -type f -name '*.old' -delete", shell=True)
        run_command("find /var/log -type f -name '*.1' -delete", shell=True)
        run_command("find /var/log -type f -name '*.2' -delete", shell=True)
        print("Old logs removed")

def perform_cleaning(dry_run=False):
    """
    Perform actual cleaning operations.
    
    Args:
        dry_run: If True, only show what would be cleaned
    """
    if dry_run:
        print("\nDRY RUN MODE - No files will be deleted\n")
    
    if not is_root() and not dry_run:
        print("\nWARNING: Not running as root - some operations may fail")
        print("Run with sudo for complete system cleaning\n")
    
    print_header("System Cleaning")
    
    # Scan items
    print("Scanning system for cleanable items...\n")
    cleanable = scan_cleanable_items()
    
    # Show summary
    show_cleanable_summary(cleanable)
    
    # Calculate total
    total = sum(cleanable.values())
    print_subheader("Summary")
    print_key_value("Total Cleanable Space", format_bytes(total))
    
    if dry_run:
        print("\nDry run complete - no files were deleted")
        return
    
    # Ask for confirmation
    print("\nProceed with cleaning? (y/n): ", end='')
    response = input().strip().lower()
    
    if response != 'y':
        print("Cleaning cancelled")
        return
    
    print("\nStarting cleanup...\n")
    
    # Perform cleaning operations
    if 'apt_cache' in cleanable:
        clean_apt_cache()
    
    if 'dnf_cache' in cleanable:
        clean_dnf_cache()
    
    if 'yum_cache' in cleanable:
        clean_yum_cache()
    
    if 'user_cache' in cleanable:
        clean_user_cache()
    
    if 'journal_logs' in cleanable:
        clean_journal_logs()
    
    if 'old_logs' in cleanable:
        clean_old_logs()
    
    print("\nCleaning completed!")
    
    # Rescan to show freed space
    print("\nRescanning...")
    new_cleanable = scan_cleanable_items()
    new_total = sum(new_cleanable.values())
    freed = total - new_total
    
    print_key_value("Space Freed", format_bytes(freed))
    print()
