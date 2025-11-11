import sqlite3
from datetime import datetime
from typing import List, Tuple

class HistoryDB:
    def __init__(self, db_path: str = "history.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_query TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                code_snippet TEXT,
                language TEXT
            )
        """)
        conn.commit()
        conn.close()
    
    def add_conversation(self, user_query: str, ai_response: str, 
                        code_snippet: str = None, language: str = None):
        """Store a conversation turn"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO conversations (timestamp, user_query, ai_response, code_snippet, language)
            VALUES (?, ?, ?, ?, ?)
        """, (datetime.now().isoformat(), user_query, ai_response, code_snippet, language))
        conn.commit()
        conn.close()
    
    def get_all_conversations(self) -> List[Tuple]:
        """Retrieve all conversation history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM conversations ORDER BY timestamp DESC")
        results = cursor.fetchall()
        conn.close()
        return results
    
    def search_by_keyword(self, keyword: str) -> List[Tuple]:
        """Search conversations by keyword"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM conversations 
            WHERE user_query LIKE ? OR ai_response LIKE ? OR code_snippet LIKE ?
            ORDER BY timestamp DESC
        """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        results = cursor.fetchall()
        conn.close()
        return results
    
    def clear_all(self):
        """Clear all conversation history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM conversations")
        conn.commit()
        conn.close()
    
    def delete_conversation(self, conversation_id: int):
        """Delete a specific conversation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
        conn.commit()
        conn.close()
    
    def get_stats(self):
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total conversations
        cursor.execute("SELECT COUNT(*) FROM conversations")
        total = cursor.fetchone()[0]
        
        # Conversations by language
        cursor.execute("""
            SELECT language, COUNT(*) 
            FROM conversations 
            WHERE language IS NOT NULL 
            GROUP BY language
        """)
        by_language = cursor.fetchall()
        
        conn.close()
        return {"total": total, "by_language": dict(by_language)}
