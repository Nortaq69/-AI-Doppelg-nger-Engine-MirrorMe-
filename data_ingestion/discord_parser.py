"""
Discord Parser
Extracts and processes Discord message data from exports
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class DiscordParser:
    """Parses Discord export data to extract user messages and personality traits"""
    
    def __init__(self):
        self.user_id = None
        self.user_name = None
        self.processed_messages = []
        
    async def parse_export(self, export_path: str) -> List[Dict[str, Any]]:
        """Parse Discord export directory and extract user messages"""
        export_dir = Path(export_path)
        
        if not export_dir.exists():
            logger.error(f"Discord export directory not found: {export_path}")
            return []
        
        logger.info(f"📱 Parsing Discord export from: {export_path}")
        
        # Find and parse messages
        messages = []
        
        # Look for message files in the export
        for file_path in export_dir.rglob("*.json"):
            if "messages" in file_path.name.lower():
                try:
                    file_messages = await self._parse_message_file(file_path)
                    messages.extend(file_messages)
                except Exception as e:
                    logger.error(f"Failed to parse {file_path}: {e}")
        
        # Also look for CSV files (alternative export format)
        for file_path in export_dir.rglob("*.csv"):
            if "messages" in file_path.name.lower():
                try:
                    file_messages = await self._parse_csv_file(file_path)
                    messages.extend(file_messages)
                except Exception as e:
                    logger.error(f"Failed to parse {file_path}: {e}")
        
        # Filter for user's own messages
        user_messages = await self._filter_user_messages(messages)
        
        logger.info(f"📱 Found {len(user_messages)} user messages from Discord")
        return user_messages
    
    async def _parse_message_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse a Discord message JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            messages = []
            
            # Handle different Discord export formats
            if isinstance(data, list):
                # Direct message array
                messages = data
            elif isinstance(data, dict):
                # Channel/thread format
                if "messages" in data:
                    messages = data["messages"]
                elif "channel" in data and "messages" in data["channel"]:
                    messages = data["channel"]["messages"]
            
            return messages
            
        except Exception as e:
            logger.error(f"Failed to parse JSON file {file_path}: {e}")
            return []
    
    async def _parse_csv_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse a Discord message CSV file"""
        try:
            import csv
            
            messages = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    message = {
                        "id": row.get("ID", ""),
                        "timestamp": row.get("Timestamp", ""),
                        "content": row.get("Content", ""),
                        "author": {
                            "id": row.get("Author ID", ""),
                            "name": row.get("Author", "")
                        },
                        "channel_id": row.get("Channel ID", ""),
                        "attachments": []
                    }
                    messages.append(message)
            
            return messages
            
        except Exception as e:
            logger.error(f"Failed to parse CSV file {file_path}: {e}")
            return []
    
    async def _filter_user_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter messages to only include those from the user"""
        user_messages = []
        
        # First pass: identify the user
        if not self.user_id:
            await self._identify_user(messages)
        
        # Filter messages by user
        for msg in messages:
            if self._is_user_message(msg):
                processed_msg = await self._process_message(msg)
                if processed_msg:
                    user_messages.append(processed_msg)
        
        return user_messages
    
    async def _identify_user(self, messages: List[Dict[str, Any]]):
        """Identify the user from the message data"""
        # Look for patterns that indicate the user
        # This is a simplified approach - in practice, you'd need more sophisticated detection
        
        # Count message frequency by author
        author_counts = {}
        for msg in messages:
            author_id = msg.get("author", {}).get("id", "")
            if author_id:
                author_counts[author_id] = author_counts.get(author_id, 0) + 1
        
        # Assume the most frequent author is the user
        if author_counts:
            self.user_id = max(author_counts, key=author_counts.get)
            
            # Get the user's name
            for msg in messages:
                if msg.get("author", {}).get("id") == self.user_id:
                    self.user_name = msg.get("author", {}).get("name", "Unknown")
                    break
            
            logger.info(f"👤 Identified user: {self.user_name} (ID: {self.user_id})")
    
    def _is_user_message(self, message: Dict[str, Any]) -> bool:
        """Check if a message is from the user"""
        if not self.user_id:
            return False
        
        author_id = message.get("author", {}).get("id", "")
        return author_id == self.user_id
    
    async def _process_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process a single message for personality analysis"""
        try:
            content = message.get("content", "").strip()
            
            # Skip empty messages or system messages
            if not content or content.startswith("**"):
                return None
            
            # Parse timestamp
            timestamp = message.get("timestamp", "")
            if timestamp:
                try:
                    # Handle different timestamp formats
                    if timestamp.endswith("Z"):
                        timestamp = timestamp[:-1] + "+00:00"
                    parsed_time = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                except:
                    parsed_time = None
            else:
                parsed_time = None
            
            # Extract context
            context = self._extract_context(message)
            
            # Process attachments
            attachments = message.get("attachments", [])
            attachment_text = self._process_attachments(attachments)
            
            # Combine content with attachment text
            full_content = content
            if attachment_text:
                full_content += f"\n[Attachments: {attachment_text}]"
            
            processed_message = {
                "id": message.get("id", ""),
                "content": full_content,
                "timestamp": parsed_time.isoformat() if parsed_time else None,
                "context": context,
                "platform": "discord",
                "channel": message.get("channel_id", ""),
                "attachments": len(attachments),
                "reactions": len(message.get("reactions", [])),
                "mentions": len(message.get("mentions", [])),
                "edited": message.get("edited", False)
            }
            
            return processed_message
            
        except Exception as e:
            logger.error(f"Failed to process message: {e}")
            return None
    
    def _extract_context(self, message: Dict[str, Any]) -> str:
        """Extract context from a message"""
        context_parts = []
        
        # Channel context
        channel_id = message.get("channel_id", "")
        if channel_id:
            context_parts.append(f"channel:{channel_id}")
        
        # Thread context
        if "thread" in message:
            context_parts.append("thread")
        
        # Reply context
        if "referenced_message" in message:
            context_parts.append("reply")
        
        # DM vs server context
        if channel_id and len(channel_id) > 20:  # Rough heuristic for DM channels
            context_parts.append("dm")
        else:
            context_parts.append("server")
        
        return "|".join(context_parts)
    
    def _process_attachments(self, attachments: List[Dict[str, Any]]) -> str:
        """Process message attachments"""
        if not attachments:
            return ""
        
        attachment_types = []
        for attachment in attachments:
            filename = attachment.get("filename", "")
            if filename:
                ext = Path(filename).suffix.lower()
                if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                    attachment_types.append("image")
                elif ext in ['.mp4', '.mov', '.avi', '.webm']:
                    attachment_types.append("video")
                elif ext in ['.mp3', '.wav', '.ogg']:
                    attachment_types.append("audio")
                else:
                    attachment_types.append("file")
        
        return ", ".join(set(attachment_types))
    
    def get_user_info(self) -> Dict[str, str]:
        """Get identified user information"""
        return {
            "id": self.user_id,
            "name": self.user_name
        }
    
    def get_message_stats(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get statistics about the user's messages"""
        if not messages:
            return {}
        
        total_messages = len(messages)
        total_chars = sum(len(msg.get("content", "")) for msg in messages)
        avg_length = total_chars / total_messages if total_messages > 0 else 0
        
        # Count emojis
        emoji_count = 0
        for msg in messages:
            content = msg.get("content", "")
            emoji_count += len(re.findall(r'<a?:.+?:\d+>', content))  # Discord emojis
            emoji_count += len(re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002600-\U000027BF]', content))  # Unicode emojis
        
        # Context breakdown
        contexts = {}
        for msg in messages:
            context = msg.get("context", "")
            contexts[context] = contexts.get(context, 0) + 1
        
        return {
            "total_messages": total_messages,
            "total_characters": total_chars,
            "average_length": round(avg_length, 2),
            "emoji_count": emoji_count,
            "context_breakdown": contexts
        } 