#!/usr/bin/env python3
"""
Hackathon Finder - Cron Job Setup Script
This script sets up a cron job to run the daily_update.sh script every day at midnight.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("cron_setup.log"), logging.StreamHandler()]
)
logger = logging.getLogger("cron_setup")

def setup_cron_job():
    """Set up a cron job to run the daily_update.sh script every day at midnight."""
    try:
        # Get the absolute path to the daily_update.sh script
        script_dir = Path(__file__).resolve().parent
        update_script = script_dir / "daily_update.sh"
        
        # Make sure the update script is executable
        os.chmod(update_script, 0o755)
        logger.info(f"Made {update_script} executable")
        
        # Create a temporary file with the current crontab
        subprocess.run("crontab -l > /tmp/current_crontab 2>/dev/null || true", shell=True, check=True)
        
        # Check if the job already exists
        with open("/tmp/current_crontab", "r") as f:
            current_crontab = f.read()
        
        if str(update_script) in current_crontab:
            logger.info("Cron job already exists, skipping")
            return
        
        # Add the new job to the crontab
        with open("/tmp/current_crontab", "a") as f:
            f.write(f"\n# Run hackathon updater daily at midnight\n0 0 * * * {update_script}\n")
        
        # Install the new crontab
        subprocess.run("crontab /tmp/current_crontab", shell=True, check=True)
        
        # Clean up
        os.unlink("/tmp/current_crontab")
        
        logger.info("Cron job set up successfully")
        print("Cron job set up successfully. The hackathon data will be updated daily at midnight.")
    except Exception as e:
        logger.error(f"Error setting up cron job: {e}")
        print(f"Error setting up cron job: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_cron_job()
