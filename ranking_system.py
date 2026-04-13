import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
import json

class RankingSystem:
    def __init__(self, database):
        self.db = database
        
    def calculate_success_rate(self, excuse_data):
        """Calculate success rate for an excuse"""
        if excuse_data['total_uses'] == 0:
            return 0
        return (excuse_data['successful_uses'] / excuse_data['total_uses']) * 100
    
    def calculate_recency_score(self, last_used):
        """Calculate recency score (more recent = higher score)"""
        if not last_used:
            return 0
        
        try:
            if isinstance(last_used, str):
                last_used = datetime.fromisoformat(last_used.replace(' ', 'T'))
            
            days_ago = (datetime.now() - last_used).days
            # Exponential decay: more recent = higher score
            score = max(0, 100 * np.exp(-days_ago / 30))
            return score
        except:
            return 50
    
    def rank_excuses(self, scenario, limit=10):
        """Rank excuses by effectiveness for a specific scenario"""
        conn = self.db.db_path
        import sqlite3
        
        with sqlite3.connect(conn) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT id, excuse_text, success_count, used_count, believability_score, last_used
                FROM excuse_history 
                WHERE scenario LIKE ?
                ORDER BY used_count DESC
                LIMIT 20
            ''', (f'%{scenario}%',))
            
            results = cursor.fetchall()
        
        ranked_excuses = []
        for row in results:
            excuse_id, text, success, used, believability, last_used = row
            
            success_rate = (success / used) * 100 if used > 0 else 0
            
            # Combine metrics for final score
            # 50% success rate, 30% believability, 20% recency
            recency_score = self.calculate_recency_score(last_used)
            
            final_score = (
                success_rate * 0.5 +
                believability * 0.3 +
                recency_score * 0.2
            )
            
            ranked_excuses.append({
                'id': excuse_id,
                'excuse': text,
                'success_rate': round(success_rate, 1),
                'believability': believability,
                'times_used': used,
                'times_successful': success,
                'score': round(final_score, 1),
                'rank': 0  # Will set after sorting
            })
        
        # Sort by score and assign ranks
        ranked_excuses.sort(key=lambda x: x['score'], reverse=True)
        for i, excuse in enumerate(ranked_excuses[:limit]):
            excuse['rank'] = i + 1
        
        return ranked_excuses[:limit]
    
    def get_best_excuse_for_scenario(self, scenario):
        """Get the single best excuse for a scenario"""
        ranked = self.rank_excuses(scenario, limit=1)
        if ranked:
            return ranked[0]
        return None
    
    def get_trending_excuses(self, days=7):
        """Get excuses that have been most successful recently"""
        conn = self.db.db_path
        import sqlite3
        
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        with sqlite3.connect(conn) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT excuse_text, success_count, used_count, believability_score
                FROM excuse_history 
                WHERE last_used > ?
                ORDER BY (success_count * 1.0 / used_count) DESC
                LIMIT 10
            ''', (cutoff_date,))
            
            results = cursor.fetchall()
        
        trending = []
        for text, success, used, believability in results:
            success_rate = (success / used) * 100 if used > 0 else 0
            trending.append({
                'excuse': text,
                'success_rate': round(success_rate, 1),
                'believability': believability,
                'trending_score': round(success_rate * 0.7 + believability * 0.3, 1)
            })
        
        return trending
    
    def compare_excuses(self, excuse1_id, excuse2_id):
        """Compare two excuses side by side"""
        conn = self.db.db_path
        import sqlite3
        
        with sqlite3.connect(conn) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT excuse_text, success_count, used_count, believability_score
                FROM excuse_history WHERE id = ?
            ''', (excuse1_id,))
            excuse1 = cursor.fetchone()
            
            cursor.execute('''
                SELECT excuse_text, success_count, used_count, believability_score
                FROM excuse_history WHERE id = ?
            ''', (excuse2_id,))
            excuse2 = cursor.fetchone()
        
        if not excuse1 or not excuse2:
            return None
        
        rate1 = (excuse1[1] / excuse1[2]) * 100 if excuse1[2] > 0 else 0
        rate2 = (excuse2[1] / excuse2[2]) * 100 if excuse2[2] > 0 else 0
        
        comparison = {
            'excuse1': {
                'text': excuse1[0],
                'success_rate': round(rate1, 1),
                'believability': excuse1[3],
                'total_uses': excuse1[2]
            },
            'excuse2': {
                'text': excuse2[0],
                'success_rate': round(rate2, 1),
                'believability': excuse2[3],
                'total_uses': excuse2[2]
            },
            'verdict': 'Excuse 1 is better' if rate1 > rate2 else 'Excuse 2 is better'
        }
        
        return comparison

# Initialize ranking system (will be used with database)