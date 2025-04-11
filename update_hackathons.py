#!/usr/bin/env python3
"""
Hackathon Finder - API-based Data Collection Script
This script collects hackathon data from various APIs and updates the GitHub repository
with the latest information, prioritizing California and online events sorted by newest dates.
"""

import os
import json
import requests
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("hackathon_updater.log"), logging.StreamHandler()]
)
logger = logging.getLogger("hackathon_updater")

# API Configuration
DEVPOST_API_BASE = "https://api.devpost.com/hackathons"  # Example API endpoint
MLH_API_BASE = "https://api.mlh.io/v1/events"  # Example API endpoint
LUMA_API_BASE = "https://api.lu.ma/public/v1"  # Confirmed API endpoint
DEV_EVENTS_API_BASE = "https://api.dev.events/hackathons"  # Example API endpoint

# Configuration for API keys (would be stored in environment variables in production)
API_KEYS = {
    "devpost": os.environ.get("DEVPOST_API_KEY", ""),
    "mlh": os.environ.get("MLH_API_KEY", ""),
    "luma": os.environ.get("LUMA_API_KEY", ""),
    "dev_events": os.environ.get("DEV_EVENTS_API_KEY", "")
}

class HackathonEvent:
    """Class representing a hackathon event with all necessary details."""
    
    def __init__(
        self,
        title: str,
        start_date: str,
        end_date: str,
        location: str,
        url: str,
        platform: str,
        is_online: bool = False,
        is_california: bool = False,
        prize: Optional[str] = None,
        tags: Optional[List[str]] = None
    ):
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.url = url
        self.platform = platform
        self.is_online = is_online
        self.is_california = is_california
        self.prize = prize
        self.tags = tags or []
        
        # Parse dates for sorting
        try:
            self.start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        except (ValueError, TypeError):
            self.start_date_obj = datetime.max
    
    def __lt__(self, other):
        """Enable sorting by start date (newest first)."""
        return self.start_date_obj > other.start_date_obj
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "title": self.title,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "location": self.location,
            "url": self.url,
            "platform": self.platform,
            "is_online": self.is_online,
            "is_california": self.is_california,
            "prize": self.prize,
            "tags": self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HackathonEvent':
        """Create instance from dictionary."""
        return cls(
            title=data["title"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            location=data["location"],
            url=data["url"],
            platform=data["platform"],
            is_online=data["is_online"],
            is_california=data["is_california"],
            prize=data.get("prize"),
            tags=data.get("tags", [])
        )


class HackathonCollector:
    """Base class for collecting hackathon data from APIs."""
    
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        
    def fetch_hackathons(self) -> List[HackathonEvent]:
        """Fetch hackathons from the API. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement fetch_hackathons")


class DevpostCollector(HackathonCollector):
    """Collector for Devpost hackathons."""
    
    def fetch_hackathons(self) -> List[HackathonEvent]:
        """Fetch hackathons from Devpost API."""
        logger.info("Fetching hackathons from Devpost API")
        try:
            # In a real implementation, this would use the actual Devpost API
            # For now, we'll simulate the API response
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
                
            # Simulated API call
            # response = requests.get(
            #     f"{DEVPOST_API_BASE}?filter=online&sort=newest",
            #     headers=headers
            # )
            # response.raise_for_status()
            # data = response.json()
            
            # Simulated data for demonstration
            simulated_data = [
                {
                    "title": "MAIS202 Final Projects: Winter 2025",
                    "start_date": "2025-04-09",
                    "end_date": "2025-04-10",
                    "location": "Online",
                    "url": "https://devpost.com/hackathons?challenge_type[]=online&order_by=recently-added",
                    "platform": "Devpost",
                    "is_online": True,
                    "prize": "Non-cash prizes"
                },
                {
                    "title": "Bitcoin 2025 Official Hackathon",
                    "start_date": "2025-04-08",
                    "end_date": "2025-05-20",
                    "location": "Online",
                    "url": "https://devpost.com/hackathons?challenge_type[]=online&order_by=recently-added",
                    "platform": "Devpost",
                    "is_online": True,
                    "prize": "$32,000"
                },
                {
                    "title": "Agentforce Virtual Hackathon",
                    "start_date": "2025-03-05",
                    "end_date": "2025-04-30",
                    "location": "Online",
                    "url": "https://devpost.com/hackathons?challenge_type[]=online&order_by=recently-added",
                    "platform": "Devpost",
                    "is_online": True,
                    "prize": "$140,000",
                    "tags": ["AI", "Machine Learning"]
                }
            ]
            
            return [
                HackathonEvent(
                    title=item["title"],
                    start_date=item["start_date"],
                    end_date=item["end_date"],
                    location=item["location"],
                    url=item["url"],
                    platform=item["platform"],
                    is_online=item["is_online"],
                    is_california="California" in item["location"],
                    prize=item.get("prize"),
                    tags=item.get("tags", [])
                )
                for item in simulated_data
            ]
        except Exception as e:
            logger.error(f"Error fetching Devpost hackathons: {e}")
            return []


class MLHCollector(HackathonCollector):
    """Collector for MLH hackathons."""
    
    def fetch_hackathons(self) -> List[HackathonEvent]:
        """Fetch hackathons from MLH API."""
        logger.info("Fetching hackathons from MLH API")
        try:
            # In a real implementation, this would use the actual MLH API
            # For now, we'll simulate the API response
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
                
            # Simulated API call
            # response = requests.get(
            #     f"{MLH_API_BASE}?season=2025",
            #     headers=headers
            # )
            # response.raise_for_status()
            # data = response.json()
            
            # Simulated data for demonstration
            simulated_data = [
                {
                    "title": "Bit Hacks",
                    "start_date": "2025-04-11",
                    "end_date": "2025-04-13",
                    "location": "Irvine, California",
                    "url": "https://mlh.io/seasons/2025/events",
                    "platform": "MLH",
                    "is_online": False,
                    "is_california": True
                },
                {
                    "title": "CruzHacks",
                    "start_date": "2025-04-11",
                    "end_date": "2025-04-13",
                    "location": "Santa Cruz, California",
                    "url": "https://mlh.io/seasons/2025/events",
                    "platform": "MLH",
                    "is_online": False,
                    "is_california": True
                },
                {
                    "title": "AI Hackfest",
                    "start_date": "2025-04-11",
                    "end_date": "2025-04-13",
                    "location": "Online",
                    "url": "https://mlh.io/seasons/2025/events",
                    "platform": "MLH",
                    "is_online": True,
                    "tags": ["AI"]
                },
                {
                    "title": "Global Hack Week: API",
                    "start_date": "2025-04-11",
                    "end_date": "2025-04-17",
                    "location": "Online",
                    "url": "https://mlh.io/seasons/2025/events",
                    "platform": "MLH",
                    "is_online": True,
                    "tags": ["API"]
                }
            ]
            
            return [
                HackathonEvent(
                    title=item["title"],
                    start_date=item["start_date"],
                    end_date=item["end_date"],
                    location=item["location"],
                    url=item["url"],
                    platform=item["platform"],
                    is_online=item["is_online"],
                    is_california=item.get("is_california", False),
                    tags=item.get("tags", [])
                )
                for item in simulated_data
            ]
        except Exception as e:
            logger.error(f"Error fetching MLH hackathons: {e}")
            return []


class LumaCollector(HackathonCollector):
    """Collector for Lu.ma hackathons."""
    
    def fetch_hackathons(self) -> List[HackathonEvent]:
        """Fetch hackathons from Lu.ma API."""
        logger.info("Fetching hackathons from Lu.ma API")
        try:
            # In a real implementation, this would use the actual Lu.ma API
            # For now, we'll simulate the API response
            if not self.api_key:
                logger.warning("No Lu.ma API key provided, skipping")
                return []
                
            headers = {
                "x-luma-api-key": self.api_key
            }
                
            # Simulated API call
            # response = requests.get(
            #     f"{LUMA_API_BASE}/calendar/list-events?filter=hackathon",
            #     headers=headers
            # )
            # response.raise_for_status()
            # data = response.json()
            
            # Simulated data for demonstration
            simulated_data = [
                {
                    "title": "AI Agent Hackathon",
                    "start_date": "2025-05-15",
                    "end_date": "2025-05-16",
                    "location": "Online",
                    "url": "https://lu.ma/t56zq6ud",
                    "platform": "Lu.ma",
                    "is_online": True,
                    "tags": ["AI", "Agents"]
                },
                {
                    "title": "SF Climate Week 2025 Energy Hackathon",
                    "start_date": "2025-06-10",
                    "end_date": "2025-06-11",
                    "location": "San Francisco, California",
                    "url": "https://lu.ma/pwh9o2e8",
                    "platform": "Lu.ma",
                    "is_online": False,
                    "is_california": True,
                    "tags": ["Climate", "Energy"]
                }
            ]
            
            return [
                HackathonEvent(
                    title=item["title"],
                    start_date=item["start_date"],
                    end_date=item["end_date"],
                    location=item["location"],
                    url=item["url"],
                    platform=item["platform"],
                    is_online=item["is_online"],
                    is_california=item.get("is_california", False),
                    tags=item.get("tags", [])
                )
                for item in simulated_data
            ]
        except Exception as e:
            logger.error(f"Error fetching Lu.ma hackathons: {e}")
            return []


class DevEventsCollector(HackathonCollector):
    """Collector for dev.events hackathons."""
    
    def fetch_hackathons(self) -> List[HackathonEvent]:
        """Fetch hackathons from dev.events API."""
        logger.info("Fetching hackathons from dev.events API")
        try:
            # In a real implementation, this would use the actual dev.events API
            # For now, we'll simulate the API response
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
                
            # Simulated API call
            # response = requests.get(
            #     f"{DEV_EVENTS_API_BASE}/NA/US/CA",
            #     headers=headers
            # )
            # response.raise_for_status()
            # data = response.json()
            
            # Simulated data for demonstration
            simulated_data = [
                {
                    "title": "Hack Cupertino 2025",
                    "start_date": "2025-04-12",
                    "end_date": "2025-04-13",
                    "location": "Cupertino, California",
                    "url": "https://dev.events/hackathons/NA/US/CA",
                    "platform": "dev.events",
                    "is_online": False,
                    "is_california": True,
                    "tags": ["Tech"]
                }
            ]
            
            return [
                HackathonEvent(
                    title=item["title"],
                    start_date=item["start_date"],
                    end_date=item["end_date"],
                    location=item["location"],
                    url=item["url"],
                    platform=item["platform"],
                    is_online=item["is_online"],
                    is_california=item["is_california"],
                    tags=item.get("tags", [])
                )
                for item in simulated_data
            ]
        except Exception as e:
            logger.error(f"Error fetching dev.events hackathons: {e}")
            return []


class HackathonUpdater:
    """Main class for updating hackathon data in the GitHub repository."""
    
    def __init__(self, collectors: List[HackathonCollector], data_file: str = "hackathons.json"):
        self.collectors = collectors
        self.data_file = data_file
        self.hackathons = []
        
    def collect_all_hackathons(self) -> List[HackathonEvent]:
        """Collect hackathons from all sources."""
        all_hackathons = []
        for collector in self.collectors:
            hackathons = collector.fetch_hackathons()
            all_hackathons.extend(hackathons)
        return all_hackathons
    
    def filter_and_sort_hackathons(self, hackathons: List[HackathonEvent]) -> Dict[str, List[HackathonEvent]]:
        """Filter and sort hackathons by category."""
        # Sort all hackathons by start date (newest first)
        sorted_hackathons = sorted(hackathons)
        
        # Filter by category
        california_hackathons = [h for h in sorted_hackathons if h.is_california]
        online_hackathons = [h for h in sorted_hackathons if h.is_online]
        other_hackathons = [h for h in sorted_hackathons if not h.is_california and not h.is_online]
        
        return {
            "california": california_hackathons,
            "online": online_hackathons,
            "other": other_hackathons
        }
    
    def save_hackathons_to_json(self, categorized_hackathons: Dict[str, List[HackathonEvent]]) -> None:
        """Save hackathons to JSON file."""
        data = {
            category: [h.to_dict() for h in hackathons]
            for category, hackathons in categorized_hackathons.items()
        }
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Saved hackathon data to {self.data_file}")
    
    def generate_readme_content(self, categorized_hackathons: Dict[str, List[HackathonEvent]]) -> str:
        """Generate README.md content with hackathon tables."""
        template = """# Hackathon Finder 2025

A curated list of top-rated hackathons with priority for California and online events, sorted by newest dates. This repository is maintained to help developers find the best hackathon opportunities.

🔍 **Priority Focus**: California-based and online hackathons  
📅 **Sorting**: Newest events first  
🏆 **Quality**: Emphasis on top-rated events

## How to Use This Repository

- Browse the tables below to find hackathons that match your interests
- Click the "Apply" button to go directly to the application page
- Check back regularly as this list is updated with new events
- Archived past events can be found in [ARCHIVE.md](./ARCHIVE.md)

---
## The List 🧑‍💻

<!-- Please leave a one line gap between this and the table TABLE_START (DO NOT CHANGE THIS LINE) -->

# California Hackathons
| Hackathon | Date | Location | Application/Link |
| --------- | ---- | -------- | ---------------- |
{california_hackathons}

<!-- Please leave a one line gap between this and the table TABLE_END (DO NOT CHANGE THIS LINE) -->

<!-- Please leave a one line gap between this and the table TABLE_START (DO NOT CHANGE THIS LINE) -->

# Online Hackathons
| Hackathon | Date | Platform | Application/Link |
| --------- | ---- | -------- | ---------------- |
{online_hackathons}

<!-- Please leave a one line gap between this and the table TABLE_END (DO NOT CHANGE THIS LINE) -->

<!-- Please leave a one line gap between this and the table TABLE_START (DO NOT CHANGE THIS LINE) -->

# Other Hackathons
| Hackathon | Date | Location | Application/Link |
| --------- | ---- | -------- | ---------------- |
{other_hackathons}

<!-- Please leave a one line gap between this and the table TABLE_END (DO NOT CHANGE THIS LINE) -->

## Contribute to the hackathon finder ❤️

Found a hackathon that should be on this list? Please submit an issue with the following information:
- Hackathon name
- Date
- Location (California or Online preferred)
- Application link
- Any additional details (prizes, themes, etc.)

## Acknowledgements

This repository is inspired by [amahjoor/Hackathons](https://github.com/amahjoor/Hackathons) and uses data from multiple sources including:
- [Devpost](https://devpost.com/hackathons)
- [Major League Hacking (MLH)](https://mlh.io/seasons/2025/events)
- [dev.events](https://dev.events/hackathons/NA/US/CA)
- [Lu.ma](https://lu.ma) (requires Luma Plus subscription for API access)

Special thanks to everyone who organizes and sponsors hackathons, making these opportunities available to developers worldwide.

---
*Last updated: {update_date}*
"""
        
        # Format hackathon rows
        california_rows = []
        for h in categorized_hackathons["california"]:
            date_str = f"{h.start_date} - {h.end_date}" if h.end_date else h.start_date
            row = f"| **[{h.title}]({h.url})** | {date_str} | {h.location} | <a href=\"{h.url}\" target=\"_blank\"><img src=\"https://i.imgur.com/w6lyvuC.png\" width=\"84\" alt=\"Apply\"></a> |"
            california_rows.append(row)
        
        online_rows = []
        for h in categorized_hackathons["online"]:
            date_str = f"{h.start_date} - {h.end_date}" if h.end_date else h.start_date
            row = f"| **[{h.title}]({h.url})** | {date_str} | {h.platform} | <a href=\"{h.url}\" target=\"_blank\"><img src=\"https://i.imgur.com/w6lyvuC.png\" width=\"84\" alt=\"Apply\"></a> |"
            online_rows.append(row)
        
        other_rows = []
        for h in categorized_hackathons["other"]:
            date_str = f"{h.start_date} - {h.end_date}" if h.end_date else h.start_date
            row = f"| **[{h.title}]({h.url})** | {date_str} | {h.location} | <a href=\"{h.url}\" target=\"_blank\"><img src=\"https://i.imgur.com/w6lyvuC.png\" width=\"84\" alt=\"Apply\"></a> |"
            other_rows.append(row)
        
        # Fill in template
        content = template.format(
            california_hackathons="\n".join(california_rows) if california_rows else "| No California hackathons found | | | |",
            online_hackathons="\n".join(online_rows) if online_rows else "| No online hackathons found | | | |",
            other_hackathons="\n".join(other_rows) if other_rows else "| No other hackathons found | | | |",
            update_date=datetime.now().strftime("%Y-%m-%d")
        )
        
        return content
    
    def update_readme(self, categorized_hackathons: Dict[str, List[HackathonEvent]]) -> None:
        """Update README.md with hackathon tables."""
        content = self.generate_readme_content(categorized_hackathons)
        
        with open("README.md", 'w') as f:
            f.write(content)
        
        logger.info("Updated README.md with hackathon tables")
    
    def update_archive(self, categorized_hackathons: Dict[str, List[HackathonEvent]]) -> None:
        """Update ARCHIVE.md with past hackathons."""
        # In a real implementation, this would move past hackathons to ARCHIVE.md
        # For now, we'll create a simple archive file
        content = """# Archived Hackathons

This file contains past hackathons that are no longer active.

## Past Hackathons

| Hackathon | Date | Location | Platform |
| --------- | ---- | -------- | -------- |
| Example Past Hackathon | 2024-12-01 - 2024-12-02 | San Francisco, California | Devpost |

"""
        
        with open("ARCHIVE.md", 'w') as f:
            f.write(content)
        
        logger.info("Updated ARCHIVE.md with past hackathons")
    
    def run(self) -> None:
        """Run the hackathon update process."""
        logger.info("Starting hackathon update process")
        
        # Collect hackathons from all sources
        all_hackathons = self.collect_all_hackathons()
        logger.info(f"Collected {len(all_hackathons)} hackathons from all sources")
        
        # Filter and sort hackathons
        categorized_hackathons = self.filter_and_sort_hackathons(all_hackathons)
        logger.info(f"Categorized hackathons: {len(categorized_hackathons['california'])} California, {len(categorized_hackathons['online'])} online, {len(categorized_hackathons['other'])} other")
        
        # Save hackathons to JSON
        self.save_hackathons_to_json(categorized_hackathons)
        
        # Update README.md
        self.update_readme(categorized_hackathons)
        
        # Update ARCHIVE.md
        self.update_archive(categorized_hackathons)
        
        logger.info("Hackathon update process completed successfully")


def main():
    """Main function to run the hackathon updater."""
    # Create collectors for each source
    collectors = [
        DevpostCollector(API_KEYS["devpost"]),
        MLHCollector(API_KEYS["mlh"]),
        LumaCollector(API_KEYS["luma"]),
        DevEventsCollector(API_KEYS["dev_events"])
    ]
    
    # Create and run updater
    updater = HackathonUpdater(collectors)
    updater.run()


if __name__ == "__main__":
    main()
