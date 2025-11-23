# SysX – Terminal System Manager

[![License](https://img.shields.io/badge/license-MIT-green.svg)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)]()
[![Platform](https://img.shields.io/badge/platform-linux-lightgrey.svg)]()
[![Status](https://img.shields.io/badge/build-stable-success.svg)]()

SysX is a lightweight, terminal-based Linux utility that provides deep, structured, and highly detailed insights into your system, network, security posture, and storage health. It also includes an advanced cleaning module capable of removing cache, logs, temporary files, and residual package clutter.

---

## Prerequisites

Install the required packages before installing SysX.

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install snapd git wget python3 python3-pip -y
sudo systemctl enable --now snapd.socket
```

### Fedora

```bash
sudo dnf install snapd git wget python3 python3-pip -y
sudo ln -s /var/lib/snapd/snap /snap
sudo systemctl enable --now snapd.socket
```

### Arch / Manjaro

```bash
sudo pacman -S snapd git wget python python-pip --noconfirm
sudo systemctl enable --now snapd.socket
```

---

## Installation

You can install SysX using Snap or directly through the .snap package.

### Option 1 — Install via Snap Store

```bash
sudo snap install sysx --classic
```

### Option 2 — Install via Direct .snap Download

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

## Features

- System Information  
  CPU, memory, disk usage, kernel, hardware info, processes

- Network Information  
  Interfaces, bandwidth usage, routing tables, active connections

- Security Auditing  
  Firewall status, open ports, failed logins, running services

- System Cleaning  
  Cache cleanup, temporary files removal, log cleanup, leftover package purging

---

## Contributors

- Ayush Raj — Creator and Lead Developer  
- Contributions are welcome. Submit a Pull Request on GitHub.

---

## License

MIT License — see the LICENSE file for full details.

