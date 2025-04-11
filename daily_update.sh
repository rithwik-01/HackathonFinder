#!/bin/bash
# daily_update.sh
# This script runs the hackathon updater daily and commits changes to the repository

# Set up logging
LOG_FILE="update_log.txt"
echo "$(date): Starting daily update" >> $LOG_FILE

# Navigate to the repository directory
cd "$(dirname "$0")" || exit

# Activate virtual environment if needed
# source venv/bin/activate

# Pull latest changes from the repository
echo "Pulling latest changes..." >> $LOG_FILE
git pull origin main >> $LOG_FILE 2>&1

# Run the Python updater script
echo "Running hackathon updater..." >> $LOG_FILE
python3 update_hackathons.py >> $LOG_FILE 2>&1

# Check if there are changes to commit
if git status --porcelain | grep -q .; then
    echo "Changes detected, committing..." >> $LOG_FILE
    
    # Add all changes
    git add README.md ARCHIVE.md hackathons.json >> $LOG_FILE 2>&1
    
    # Commit with timestamp
    git commit -m "Daily update: $(date +%Y-%m-%d)" >> $LOG_FILE 2>&1
    
    # Push changes
    git push origin main >> $LOG_FILE 2>&1
    
    echo "Changes committed and pushed successfully." >> $LOG_FILE
else
    echo "No changes detected." >> $LOG_FILE
fi

echo "$(date): Daily update completed" >> $LOG_FILE
