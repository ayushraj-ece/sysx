"""
SysX - Terminal-based Linux system diagnostics and cleaning utility.

Provides detailed information about system, network, security, and storage,
with powerful cleaning capabilities for cache, logs, and temporary files.
"""

__version__ = "1.0.0"
__author__ = "SysX Contributors"
__license__ = "MIT"

from sysx.cli import main

__all__ = ['main', '__version__']
