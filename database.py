"""
Simple database module for storing user preferences
In production, you should use a proper database like PostgreSQL or SQLite
"""

import json
import os

class SimpleDatabase:
    def __init__(self, db_file: str = "user_data.json"):
        self.db_file = db_file
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {"users": {}}
        return {"users": {}}

    def _save_data(self):
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get_user_language(self, user_id):
        return self.data.get("users", {}).get(str(user_id), {}).get("language", "uz")

    def set_user_language(self, user_id, language):
        if "users" not in self.data:
            self.data["users"] = {}
        if str(user_id) not in self.data["users"]:
            self.data["users"][str(user_id)] = {}
        self.data["users"][str(user_id)]["language"] = language
        self._save_data()

    def get_user_info(self, user_id):
        return self.data.get("users", {}).get(str(user_id), {})

    def set_user_info(self, user_id, info):
        if "users" not in self.data:
            self.data["users"] = {}
        if str(user_id) not in self.data["users"]:
            self.data["users"][str(user_id)] = {}
        self.data["users"][str(user_id)].update(info)
        self._save_data()

    def get_all_users(self):
        return self.data.get("users", {})

db = SimpleDatabase()

def get_user_language(user_id):
    return db.get_user_language(user_id)

def set_user_language(user_id, language):
    db.set_user_language(user_id, language) 