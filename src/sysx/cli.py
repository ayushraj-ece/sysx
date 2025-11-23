"""
Main CLI entry point for SysX.
Handles command-line argument parsing and module dispatching.
"""

import sys
import argparse
from sysx.modules.system_info import show_system_info
from sysx.modules.network_info import show_network_info
from sysx.modules.security_check import show_security_info
from sysx.modules.cleaner import perform_cleaning

__version__ = "1.0.0"

def create_parser():
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        prog='sysx',
        description='Terminal-based Linux system diagnostics and cleaning utility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sysx system          Display system information
  sysx network         Display network information
  sysx security        Display security status
  sysx clean           Clean system (interactive)
  sysx clean --dry-run Show what would be cleaned

For more information, visit: https://github.com/yourusername/sysx
        """
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'SysX {__version__}'
    )
    
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands'
    )
    
    # System command
    subparsers.add_parser(
        'system',
        help='Display detailed system information'
    )
    
    # Network command
    subparsers.add_parser(
        'network',
        help='Display network configuration and statistics'
    )
    
    # Security command
    subparsers.add_parser(
        'security',
        help='Display security status and audit information'
    )
    
    # Clean command
    clean_parser = subparsers.add_parser(
        'clean',
        help='Clean system cache, logs, and temporary files'
    )
    clean_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be cleaned without deleting'
    )
    
    return parser

def main():
    """Main entry point for SysX CLI."""
    parser = create_parser()
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    args = parser.parse_args()
    
    try:
        # Dispatch to appropriate module
        if args.command == 'system':
            show_system_info()
        
        elif args.command == 'network':
            show_network_info()
        
        elif args.command == 'security':
            show_security_info()
        
        elif args.command == 'clean':
            perform_cleaning(dry_run=args.dry_run)
        
        else:
            parser.print_help()
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(130)
    
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
