#!/usr/bin/env python3
"""
YeldzSmart AI Browser v9.0 - Main Entry Point

Usage:
    python start.py                    # Start with default settings
    python start.py --city Delhi       # Start for specific city
    python start.py --multi-city       # Start all 8 cities in parallel
    python start.py --debug            # Enable debug mode
    python start.py --headless         # Run in headless mode

Author: YeldzSmart Team
Version: 9.0.0
Date: December 2025
"""

import os
import sys
import asyncio
import argparse
import webbrowser
from pathlib import Path
from datetime import datetime
import subprocess

# Ensure backend is in path
sys.path.insert(0, str(Path(__file__).parent))

# Color codes for terminal
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_banner():
    """Display application banner"""
    banner = f"""{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   ██╗   ██╗███████╗██╗     ██████╗ ███████╗███████╗███╗   ███╗  ║
║   ╚██╗ ██╔╝██╔════╝██║     ██╔══██╗╚══███╔╝██╔════╝████╗ ████║  ║
║    ╚████╔╝ █████╗  ██║     ██║  ██║  ███╔╝ ███████╗██╔████╔██║  ║
║     ╚██╔╝  ██╔══╝  ██║     ██║  ██║ ███╔╝  ╚════██║██║╚██╔╝██║  ║
║      ██║   ███████╗███████╗██████╔╝███████╗███████║██║ ╚═╝ ██║  ║
║      ╚═╝   ╚══════╝╚══════╝╚═════╝ ╚══════╝╚══════╝╚═╝     ╚═╝  ║
║                                                                   ║
║          🚀 AI BROWSER v9.0 - PRODUCTION READY 🚀                 ║
║          Full Automation | Anti-Ban | Multi-City                 ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.END}"""
    print(banner)

def log(message, level="INFO"):
    """Formatted logging"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    colors = {
        "INFO": Colors.CYAN,
        "SUCCESS": Colors.GREEN,
        "WARNING": Colors.YELLOW,
        "ERROR": Colors.RED
    }
    color = colors.get(level, Colors.CYAN)
    print(f"{color}[{timestamp}] [{level}] {message}{Colors.END}")

def check_dependencies():
    """Check if required dependencies are installed"""
    log("Checking dependencies...", "INFO")
    
    try:
        import fastapi
        import playwright
        log("✓ Core dependencies found", "SUCCESS")
        return True
    except ImportError as e:
        log(f"✗ Missing dependencies: {e}", "ERROR")
        log("Run: pip install -r requirements.txt", "WARNING")
        return False

def setup_directories():
    """Create necessary directories"""
    dirs = [
        "data",
        "data/exports",
        "cookies",
        "logs",
        "screenshots",
        "backend/database"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    log("✓ Directory structure ready", "SUCCESS")

async def start_backend(port=8000, debug=False):
    """Start FastAPI backend server"""
    log(f"Starting backend server on port {port}...", "INFO")
    
    try:
        cmd = [
            sys.executable, "-m", "uvicorn",
            "backend.main:app",
            "--host", "0.0.0.0",
            "--port", str(port),
            "--reload" if debug else "--no-reload"
        ]
        
        process = subprocess.Popen(cmd)
        log(f"✓ Backend started at http://localhost:{port}", "SUCCESS")
        return process
        
    except Exception as e:
        log(f"✗ Failed to start backend: {e}", "ERROR")
        return None

def open_dashboard(port=8000):
    """Open dashboard in default browser"""
    try:
        url = f"http://localhost:{port}"
        webbrowser.open(url)
        log(f"✓ Dashboard opened at {url}", "SUCCESS")
    except Exception as e:
        log(f"Could not open browser: {e}", "WARNING")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="YeldzSmart AI Browser v9.0"
    )
    parser.add_argument(
        "--city",
        type=str,
        choices=["Delhi", "Mumbai", "Pune", "Bangalore", "Lucknow", "Jaipur", "Indore", "Patna"],
        help="Start browser for specific city"
    )
    parser.add_argument(
        "--multi-city",
        action="store_true",
        help="Run all 8 cities in parallel"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run in headless mode"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Backend server port (default: 8000)"
    )
    
    args = parser.parse_args()
    
    # Display banner
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        log("Please install dependencies first!", "ERROR")
        sys.exit(1)
    
    # Setup directories
    setup_directories()
    
    # Start backend
    backend_process = asyncio.run(start_backend(args.port, args.debug))
    
    if not backend_process:
        log("Failed to start backend. Exiting.", "ERROR")
        sys.exit(1)
    
    # Wait for backend to initialize
    import time
    log("Waiting for backend to initialize...", "INFO")
    time.sleep(3)
    
    # Open dashboard
    open_dashboard(args.port)
    
    # Display usage info
    print(f"\n{Colors.GREEN}{Colors.BOLD}" + "="*70)
    log("🚀 YeldzSmart AI Browser is now running!", "SUCCESS")
    print("="*70 + Colors.END)
    print(f"\n{Colors.CYAN}Dashboard: {Colors.BOLD}http://localhost:{args.port}{Colors.END}")
    print(f"{Colors.CYAN}API Docs:  {Colors.BOLD}http://localhost:{args.port}/docs{Colors.END}")
    print(f"\n{Colors.YELLOW}Press Ctrl+C to stop{Colors.END}\n")
    
    # Keep running
    try:
        backend_process.wait()
    except KeyboardInterrupt:
        log("\nShutting down...", "WARNING")
        backend_process.terminate()
        backend_process.wait()
        log("✓ Shutdown complete", "SUCCESS")

if __name__ == "__main__":
    main()