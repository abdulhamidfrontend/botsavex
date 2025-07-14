"""
Simple database module for storing user preferences
In production, you should use a proper database like PostgreSQL or SQLite
"""

import json
import os
from typing import Dict, Any, Optional

class SimpleDatabase:
    def __init__(self, db_file: str = "user_data.json"):
        # Use absolute path for Render deployment
        if os.getenv("RENDER"):
            # On Render, use /tmp directory for file storage
            self.db_file = os.path.join("/tmp", db_file)
        else:
            self.db_file = db_file
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """Load data from JSON file"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {"users": {}, "settings": {}}
        return {"users": {}, "settings": {}}
    
    def _save_data(self):
        """Save data to JSON file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving data: {e}")
    
    def get_user_language(self, user_id: int) -> str:
        """Get user's preferred language"""
        return self.data.get("users", {}).get(str(user_id), {}).get("language", "uz")
    
    def set_user_language(self, user_id: int, language: str):
        """Set user's preferred language"""
        if "users" not in self.data:
            self.data["users"] = {}
        
        if str(user_id) not in self.data["users"]:
            self.data["users"][str(user_id)] = {}
        
        self.data["users"][str(user_id)]["language"] = language
        self._save_data()
    
    def get_user_info(self, user_id: int) -> Dict[str, Any]:
        """Get user information"""
        return self.data.get("users", {}).get(str(user_id), {})
    
    def set_user_info(self, user_id: int, info: Dict[str, Any]):
        """Set user information"""
        if "users" not in self.data:
            self.data["users"] = {}
        
        if str(user_id) not in self.data["users"]:
            self.data["users"][str(user_id)] = {}
        
        self.data["users"][str(user_id)].update(info)
        self._save_data()
    
    def get_all_users(self) -> Dict[str, Any]:
        """Get all users data"""
        return self.data.get("users", {})
    
    def delete_user(self, user_id: int):
        """Delete user data"""
        if str(user_id) in self.data.get("users", {}):
            del self.data["users"][str(user_id)]
            self._save_data()
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        return self.data.get("settings", {}).get(key, default)
    
    def set_setting(self, key: str, value: Any):
        """Set a setting value"""
        if "settings" not in self.data:
            self.data["settings"] = {}
        
        self.data["settings"][key] = value
        self._save_data()

# Global database instance
db = SimpleDatabase()

# Convenience functions
def get_user_language(user_id: int) -> str:
    """Get user's preferred language"""
    return db.get_user_language(user_id)

def set_user_language(user_id: int, language: str):
    """Set user's preferred language"""
    db.set_user_language(user_id, language)

def get_user_info(user_id: int) -> Dict[str, Any]:
    """Get user information"""
    return db.get_user_info(user_id)

def set_user_info(user_id: int, info: Dict[str, Any]):
    """Set user information"""
    db.set_user_info(user_id, info) 