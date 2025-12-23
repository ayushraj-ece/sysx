# SysX – Terminal System Manager

[![License](https://img.shields.io/badge/license-MIT-green.svg)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)]()
[![Platform](https://img.shields.io/badge/platform-linux-lightgrey.svg)]()
[![Status](https://img.shields.io/badge/build-stable-success.svg)]()

SysX is a lightweight, terminal-based Linux utility that provides deep, structured, and highly detailed insights into your system, network, security posture, and storage health. It also includes an advanced cleaning module capable of removing cache, logs, temporary files, and residual package clutter.

---

## PREREQUISITES

```bash
# Install base dependencies (works on most Linux distributions)
sudo apt install -y python3 python3-pip git 2>/dev/null || \
sudo dnf install -y python3 python3-pip git 2>/dev/null || \
sudo pacman -S --noconfirm python python-pip git

# Install pipx
python3 -m pip install --user pipx
python3 -m pipx ensurepath

```

Restart your shell if pipx is not found.

---

## INSTALLATION

```bash
curl -fsSL https://raw.githubusercontent.com/ayushraj-ece/sysx/main/scripts/install.sh | bash
```

---

## USAGE

```bash
sysx system
sysx network
sysx security
sysx clean
sysx clean --dry-run
sysx --version
```

---

## FEATURES

System Information  
CPU, memory, disk usage, kernel, hardware info, processes  

Network Information  
Interfaces, bandwidth usage, routing tables, active connections  

Security Auditing  
Firewall status, open ports, failed logins, running services  

System Cleaning  
Cache cleanup  
Temporary files removal  
Log cleanup  
Leftover package purging  

---

## CONTRIBUTORS

Ayush Raj — Creator and Lead Developer  

---

## LICENSE

MIT License — see the LICENSE file for full details.
