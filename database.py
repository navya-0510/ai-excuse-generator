import sqlite3
from datetime import datetime
import json

class ExcuseDatabase:
    def __init__(self, db_path="excuses.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize all database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table 1: Excuse History
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS excuse_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scenario TEXT NOT NULL,
                context_type TEXT NOT NULL,
                urgency TEXT NOT NULL,
                relationship TEXT NOT NULL,
                excuse_text TEXT NOT NULL,
                believability_score INTEGER DEFAULT 70,
                used_count INTEGER DEFAULT 1,
                success_count INTEGER DEFAULT 0,
                last_used TIMESTAMP,
                is_favorite BOOLEAN DEFAULT 0
            )
        ''')
        
        # Table 2: Schedule Patterns (for auto-scheduling)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedule_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day_of_week INTEGER NOT NULL,
                hour_of_day INTEGER NOT NULL,
                scenario_type TEXT NOT NULL,
                frequency INTEGER DEFAULT 1,
                last_occurrence TIMESTAMP
            )
        ''')
        
        # Table 3: Excuse Effectiveness (for ranking)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS excuse_effectiveness (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                excuse_text TEXT UNIQUE,
                total_uses INTEGER DEFAULT 0,
                successful_uses INTEGER DEFAULT 0,
                avg_believability REAL DEFAULT 0,
                last_updated TIMESTAMP
            )
        ''')
        
        # Table 4: Favorite Excuses
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS favorite_excuses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                excuse_text TEXT NOT NULL,
                category TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully")
    
    def save_excuse(self, scenario, context_type, urgency, relationship, excuse_text, believability):
        """Save generated excuse to history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO excuse_history 
            (scenario, context_type, urgency, relationship, excuse_text, believability_score, last_used)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (scenario, context_type, urgency, relationship, excuse_text, believability, datetime.now()))
        
        # Also update effectiveness table
        cursor.execute('''
            INSERT INTO excuse_effectiveness (excuse_text, total_uses, last_updated)
            VALUES (?, 1, ?)
            ON CONFLICT(excuse_text) DO UPDATE SET
            total_uses = total_uses + 1,
            last_updated = ?
        ''', (excuse_text, datetime.now(), datetime.now()))
        
        conn.commit()
        conn.close()
        return cursor.lastrowid
    
    def record_success(self, excuse_id, was_successful):
        """Record if an excuse was successful"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if was_successful:
            cursor.execute('''
                UPDATE excuse_history 
                SET success_count = success_count + 1
                WHERE id = ?
            ''', (excuse_id,))
            
            # Get excuse text for effectiveness table
            cursor.execute('SELECT excuse_text FROM excuse_history WHERE id = ?', (excuse_id,))
            result = cursor.fetchone()
            if result:
                cursor.execute('''
                    UPDATE excuse_effectiveness
                    SET successful_uses = successful_uses + 1,
                        last_updated = ?
                    WHERE excuse_text = ?
                ''', (datetime.now(), result[0]))
        
        conn.commit()
        conn.close()
    
    def get_history(self, limit=20):
        """Get recent excuse history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, scenario, context_type, excuse_text, used_count, success_count, is_favorite, last_used
            FROM excuse_history 
            ORDER BY last_used DESC 
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        history = []
        for row in results:
            history.append({
                'id': row[0],
                'scenario': row[1],
                'context': row[2],
                'excuse': row[3],
                'used': row[4],
                'successful': row[5],
                'favorite': bool(row[6]),
                'last_used': row[7]
            })
        return history
    
    def toggle_favorite(self, excuse_id):
        """Mark/unmark excuse as favorite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE excuse_history 
            SET is_favorite = NOT is_favorite
            WHERE id = ?
        ''', (excuse_id,))
        
        conn.commit()
        conn.close()
    
    def get_favorites(self):
        """Get all favorite excuses"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, excuse_text, scenario, context_type
            FROM excuse_history 
            WHERE is_favorite = 1
            ORDER BY used_count DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        favorites = []
        for row in results:
            favorites.append({
                'id': row[0],
                'excuse': row[1],
                'scenario': row[2],
                'context': row[3]
            })
        return favorites
    
    def save_pattern(self, day_of_week, hour, scenario_type):
        """Save usage pattern for auto-scheduling"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO schedule_patterns (day_of_week, hour_of_day, scenario_type, frequency, last_occurrence)
            VALUES (?, ?, ?, 1, ?)
            ON CONFLICT DO UPDATE SET
            frequency = frequency + 1,
            last_occurrence = ?
        ''', (day_of_week, hour, scenario_type, datetime.now(), datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_top_excuses(self, scenario_filter=None, limit=5):
        """Get top performing excuses by success rate"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if scenario_filter:
            cursor.execute('''
                SELECT excuse_text, success_count, used_count, believability_score
                FROM excuse_history 
                WHERE scenario LIKE ?
                ORDER BY (success_count * 1.0 / used_count) DESC, used_count DESC
                LIMIT ?
            ''', (f'%{scenario_filter}%', limit))
        else:
            cursor.execute('''
                SELECT excuse_text, success_count, used_count, believability_score
                FROM excuse_history 
                ORDER BY (success_count * 1.0 / used_count) DESC, used_count DESC
                LIMIT ?
            ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        top_excuses = []
        for idx, row in enumerate(results):
            success_rate = (row[1] / row[2]) * 100 if row[2] > 0 else 0
            top_excuses.append({
                'rank': idx + 1,
                'excuse': row[0],
                'success_rate': round(success_rate, 1),
                'times_used': row[2],
                'believability': row[3]
            })
        return top_excuses

# Initialize database
db = ExcuseDatabase()