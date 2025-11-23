"""
Plain text formatting utilities for SysX output.
No colors, no fancy formatting - just clean, readable text.
"""

def print_header(title):
    """Print main section header with equals underline."""
    print(f"\n{title.upper()}")
    print("=" * len(title))

def print_subheader(title):
    """Print subsection header with dashes underline."""
    print(f"\n{title}")
    print("-" * len(title))

def print_table(headers, rows, column_spacing=4):
    """
    Print plain text table with aligned columns.
    
    Args:
        headers: List of column header strings
        rows: List of lists containing row data
        column_spacing: Number of spaces between columns
    """
    if not rows:
        print("No data available")
        return
    
    # Calculate column widths
    widths = []
    for i in range(len(headers)):
        max_width = len(str(headers[i]))
        for row in rows:
            if i < len(row):
                max_width = max(max_width, len(str(row[i])))
        widths.append(max_width)
    
    # Print headers
    header_parts = []
    for i, header in enumerate(headers):
        header_parts.append(str(header).ljust(widths[i]))
    print((" " * column_spacing).join(header_parts))
    
    # Print rows
    for row in rows:
        row_parts = []
        for i in range(len(headers)):
            if i < len(row):
                row_parts.append(str(row[i]).ljust(widths[i]))
            else:
                row_parts.append(" " * widths[i])
        print((" " * column_spacing).join(row_parts))

def format_bytes(bytes_val):
    """
    Convert bytes to human-readable format.
    
    Args:
        bytes_val: Number of bytes
    
    Returns:
        Formatted string (e.g., "1.5 GB")
    """
    try:
        bytes_val = float(bytes_val)
    except (ValueError, TypeError):
        return "0 B"
    
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} EB"

def format_percentage(value, total):
    """
    Calculate and format percentage.
    
    Args:
        value: Current value
        total: Total value
    
    Returns:
        Percentage string (e.g., "45%")
    """
    try:
        if total == 0:
            return "0%"
        percentage = (float(value) / float(total)) * 100
        return f"{percentage:.1f}%"
    except (ValueError, TypeError, ZeroDivisionError):
        return "0%"

def format_uptime(seconds):
    """
    Convert seconds to human-readable uptime format.
    
    Args:
        seconds: Number of seconds
    
    Returns:
        Formatted string (e.g., "3 days, 14:23:15")
    """
    try:
        seconds = int(seconds)
    except (ValueError, TypeError):
        return "0:00:00"
    
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if days > 0:
        return f"{days} days, {hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def print_key_value(key, value, key_width=20):
    """
    Print key-value pair in aligned format.
    
    Args:
        key: Key string
        value: Value string
        key_width: Width for key column
    """
    print(f"{key.ljust(key_width)}: {value}")
