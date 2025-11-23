# SysX - Terminal System Manager

SysX is a lightweight, terminal-based Linux utility that provides extremely detailed information about your system, network, security status, and storage. It includes a powerful cleaning module to remove cache, logs, temporary files, and unnecessary leftovers.

## Features

- **System Information**: Detailed CPU, memory, disk, kernel, and hardware information
- **Network Information**: Interface details, active connections, routing tables, bandwidth stats
- **Security Auditing**: Firewall status, open ports, failed logins, running services
- **System Cleaning**: Remove cache, logs, temporary files, and package leftovers

## Installation

### From Snap Store

sudo snap install sysx --classic

### From Source

git clone https://github.com/ayushraj-ece/sysx.git
cd sysx
pip install -e .

## Usage

sysx system
sysx network
sysx security
sysx clean
sysx clean --dry-run
sysx --version

## Requirements

- Python 3.8+
- Linux operating system
- Root/sudo access for cleaning operations

## License

MIT License - See LICENSE file for details
