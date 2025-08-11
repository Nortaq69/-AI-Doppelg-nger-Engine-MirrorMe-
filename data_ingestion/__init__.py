"""
Data Ingestion Module
Handles collection and processing of user's digital footprint
"""

from .ingestion_manager import DataIngestionManager
from .discord_parser import DiscordParser
from .email_loader import EmailLoader
from .reddit_scraper import RedditScraper
from .text_processor import TextProcessor

__all__ = [
    'DataIngestionManager',
    'DiscordParser', 
    'EmailLoader',
    'RedditScraper',
    'TextProcessor'
] 