# SysX – Terminal System Manager

SysX is a lightweight, terminal-based Linux utility that provides deep, structured, and highly detailed insights into your system, network, security posture, and storage health. It also includes an advanced cleaning module capable of removing cache, logs, temporary files, and residual package clutter.

## Features

- **System Information**: CPU, memory, disks, kernel, hardware, and process stats  
- **Network Information**: Interfaces, routing tables, active connections, bandwidth usage  
- **Security Auditing**: Firewall status, open ports, failed logins, active services  
- **System Cleaning**: Cache cleanup, log purge, temp file removal, leftover packages  

---

## Installation

### Option 1 — Install via Snap Store

```bash
sudo snap install sysx --classic
```

---

### Option 2 — Install via Direct .snap Download (Recommended)

```bash
wget https://github.com/ayushraj-ece/sysx/releases/download/v1.0.0/sysx_1.0.0_amd64.snap
sudo snap install sysx_1.0.0_amd64.snap --dangerous --classic
```

---

## Usage

```bash
sysx system
sysx network
sysx security
sysx clean
sysx clean --dry-run
sysx --version
```

---

## Requirements

- Python 3.8+
- Linux OS
- Root/sudo access for cleaning operations

---

## License

MIT License — see LICENSE file for details.

