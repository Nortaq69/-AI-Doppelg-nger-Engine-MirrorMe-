"""
Data Ingestion Manager
Coordinates collection and processing of user's digital footprint
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio

from .discord_parser import DiscordParser
from .email_loader import EmailLoader
from .reddit_scraper import RedditScraper
from .text_processor import TextProcessor

logger = logging.getLogger(__name__)

class DataIngestionManager:
    """Manages the collection and processing of user's digital footprint"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize parsers
        self.discord_parser = DiscordParser()
        self.email_loader = EmailLoader()
        self.reddit_scraper = RedditScraper()
        self.text_processor = TextProcessor()
        
        # Data storage
        self.processed_data = {
            "messages": [],
            "emails": [],
            "posts": [],
            "personality_traits": {},
            "style_patterns": {}
        }
        
        logger.info("📥 Data Ingestion Manager initialized")
    
    async def ingest_all_sources(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest data from all configured sources"""
        logger.info("🔄 Starting comprehensive data ingestion...")
        
        results = {
            "discord": [],
            "email": [],
            "reddit": [],
            "processed": 0,
            "errors": []
        }
        
        try:
            # Discord data ingestion
            if config.get("discord", {}).get("enabled", False):
                logger.info("📱 Processing Discord data...")
                discord_data = await self.ingest_discord(config["discord"])
                results["discord"] = discord_data
            
            # Email data ingestion
            if config.get("email", {}).get("enabled", False):
                logger.info("📧 Processing email data...")
                email_data = await self.ingest_email(config["email"])
                results["email"] = email_data
            
            # Reddit data ingestion
            if config.get("reddit", {}).get("enabled", False):
                logger.info("🤖 Processing Reddit data...")
                reddit_data = await self.ingest_reddit(config["reddit"])
                results["reddit"] = reddit_data
            
            # Process and analyze all collected data
            logger.info("🧠 Analyzing personality patterns...")
            personality_data = await self.analyze_personality()
            results["personality"] = personality_data
            
            # Save processed data
            await self.save_processed_data()
            
            logger.info(f"✅ Data ingestion complete! Processed {results['processed']} items")
            
        except Exception as e:
            logger.error(f"❌ Data ingestion failed: {e}")
            results["errors"].append(str(e))
        
        return results
    
    async def ingest_discord(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Ingest Discord data from exports"""
        try:
            export_path = config.get("export_path")
            if not export_path or not Path(export_path).exists():
                logger.warning("Discord export path not found")
                return []
            
            messages = await self.discord_parser.parse_export(export_path)
            
            # Process messages for personality traits
            processed_messages = []
            for msg in messages:
                processed = self.text_processor.process_message(msg)
                if processed:
                    processed_messages.append(processed)
                    self.processed_data["messages"].append(processed)
            
            logger.info(f"📱 Processed {len(processed_messages)} Discord messages")
            return processed_messages
            
        except Exception as e:
            logger.error(f"❌ Discord ingestion failed: {e}")
            return []
    
    async def ingest_email(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Ingest email data"""
        try:
            emails = await self.email_loader.load_emails(config)
            
            # Process emails for personality traits
            processed_emails = []
            for email in emails:
                processed = self.text_processor.process_email(email)
                if processed:
                    processed_emails.append(processed)
                    self.processed_data["emails"].append(processed)
            
            logger.info(f"📧 Processed {len(processed_emails)} emails")
            return processed_emails
            
        except Exception as e:
            logger.error(f"❌ Email ingestion failed: {e}")
            return []
    
    async def ingest_reddit(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Ingest Reddit data"""
        try:
            posts = await self.reddit_scraper.scrape_user_posts(config)
            
            # Process posts for personality traits
            processed_posts = []
            for post in posts:
                processed = self.text_processor.process_post(post)
                if processed:
                    processed_posts.append(processed)
                    self.processed_data["posts"].append(processed)
            
            logger.info(f"🤖 Processed {len(processed_posts)} Reddit posts")
            return processed_posts
            
        except Exception as e:
            logger.error(f"❌ Reddit ingestion failed: {e}")
            return []
    
    async def analyze_personality(self) -> Dict[str, Any]:
        """Analyze collected data to extract personality traits"""
        try:
            # Combine all text data
            all_texts = []
            all_texts.extend([msg["content"] for msg in self.processed_data["messages"]])
            all_texts.extend([email["content"] for email in self.processed_data["emails"]])
            all_texts.extend([post["content"] for post in self.processed_data["posts"]])
            
            if not all_texts:
                logger.warning("No text data available for personality analysis")
                return {}
            
            # Analyze personality traits
            personality_traits = await self.text_processor.analyze_personality(all_texts)
            self.processed_data["personality_traits"] = personality_traits
            
            # Extract style patterns
            style_patterns = await self.text_processor.extract_style_patterns(all_texts)
            self.processed_data["style_patterns"] = style_patterns
            
            logger.info("🧠 Personality analysis complete")
            return {
                "traits": personality_traits,
                "style": style_patterns
            }
            
        except Exception as e:
            logger.error(f"❌ Personality analysis failed: {e}")
            return {}
    
    async def save_processed_data(self):
        """Save processed data to disk"""
        try:
            timestamp = datetime.now().isoformat()
            filename = f"processed_data_{timestamp}.json"
            filepath = self.data_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.processed_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Processed data saved to {filepath}")
            
        except Exception as e:
            logger.error(f"❌ Failed to save processed data: {e}")
    
    def get_personality_profile(self) -> Dict[str, Any]:
        """Get the current personality profile"""
        return {
            "traits": self.processed_data.get("personality_traits", {}),
            "style": self.processed_data.get("style_patterns", {}),
            "data_summary": {
                "messages": len(self.processed_data["messages"]),
                "emails": len(self.processed_data["emails"]),
                "posts": len(self.processed_data["posts"])
            }
        }
    
    def get_training_data(self) -> List[Dict[str, Any]]:
        """Get processed data ready for model training"""
        training_data = []
        
        # Add messages
        for msg in self.processed_data["messages"]:
            training_data.append({
                "type": "message",
                "content": msg["content"],
                "context": msg.get("context", ""),
                "timestamp": msg.get("timestamp"),
                "platform": "discord"
            })
        
        # Add emails
        for email in self.processed_data["emails"]:
            training_data.append({
                "type": "email",
                "content": email["content"],
                "context": email.get("subject", ""),
                "timestamp": email.get("timestamp"),
                "platform": "email"
            })
        
        # Add posts
        for post in self.processed_data["posts"]:
            training_data.append({
                "type": "post",
                "content": post["content"],
                "context": post.get("subreddit", ""),
                "timestamp": post.get("timestamp"),
                "platform": "reddit"
            })
        
        return training_data 