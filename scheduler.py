from datetime import datetime, timedelta
import sqlite3
import json

class AutoScheduler:
    def __init__(self, database):
        self.db = database
    
    def record_usage(self, scenario, context_type):
        """Record when an excuse is used for pattern learning"""
        now = datetime.now()
        day_of_week = now.weekday()  # 0 = Monday, 6 = Sunday
        hour = now.hour
        
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO schedule_patterns (day_of_week, hour_of_day, scenario_type, frequency, last_occurrence)
            VALUES (?, ?, ?, 1, ?)
            ON CONFLICT DO UPDATE SET
            frequency = frequency + 1,
            last_occurrence = ?
        ''', (day_of_week, hour, context_type, now, now))
        
        conn.commit()
        conn.close()
    
    def predict_next_need(self):
        """Predict when user might need an excuse next"""
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        # Get patterns for current day and time
        now = datetime.now()
        current_day = now.weekday()
        current_hour = now.hour
        
        cursor.execute('''
            SELECT scenario_type, frequency, last_occurrence
            FROM schedule_patterns
            WHERE day_of_week = ? AND hour_of_day BETWEEN ? AND ?
            ORDER BY frequency DESC
            LIMIT 3
        ''', (current_day, current_hour - 2, current_hour + 2))
        
        patterns = cursor.fetchall()
        conn.close()
        
        if patterns:
            predictions = []
            for scenario, freq, last in patterns:
                confidence = min(freq / 20, 0.95)  # Max 95% confidence
                predictions.append({
                    'scenario_type': scenario,
                    'confidence': round(confidence * 100, 1),
                    'frequency': freq,
                    'suggestion': self._generate_suggestion(scenario, confidence)
                })
            return predictions
        
        return None
    
    def _generate_suggestion(self, scenario, confidence):
        """Generate a helpful suggestion based on prediction"""
        suggestions = {
            "work": "You often need work excuses around this time. Prepare a backup excuse now.",
            "school": "Class-related excuses are common for you now. Have one ready.",
            "social": "You might need to cancel social plans. Prepare a polite excuse.",
            "family": "Family-related excuses are typical for this time. Be prepared."
        }
        
        if confidence > 0.8:
            return f"⚠️ HIGH LIKELIHOOD: {suggestions.get(scenario, 'Prepare an excuse now.')}"
        elif confidence > 0.5:
            return f"📌 MODERATE CHANCE: {suggestions.get(scenario, 'Might want a backup excuse.')}"
        else:
            return f"💡 LOW CHANCE but possible: {suggestions.get(scenario, 'Just in case, have an excuse ready.')}"
    
    def get_peak_excuse_times(self):
        """Get the times when user most frequently needs excuses"""
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT day_of_week, hour_of_day, SUM(frequency) as total_freq
            FROM schedule_patterns
            GROUP BY day_of_week, hour_of_day
            ORDER BY total_freq DESC
            LIMIT 5
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        peak_times = []
        for day_num, hour, freq in results:
            peak_times.append({
                'day': days[day_num],
                'hour': f"{hour}:00 - {hour+1}:00",
                'frequency': freq,
                'suggestion': f"Prepare excuses before {days[day_num]} at {hour}:00"
            })
        
        return peak_times
    
    def get_weekly_pattern(self):
        """Get excuse usage pattern by day of week"""
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT day_of_week, SUM(frequency) as total
            FROM schedule_patterns
            GROUP BY day_of_week
            ORDER BY day_of_week
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        pattern = []
        for i, (day_num, total) in enumerate(results):
            pattern.append({
                'day': days[day_num],
                'total_excuses': total,
                'risk_level': 'High' if total > 10 else 'Medium' if total > 5 else 'Low'
            })
        
        return pattern
    
    def set_reminder(self, hours_before=1):
        """Set a reminder to prepare an excuse"""
        prediction = self.predict_next_need()
        
        if prediction and prediction[0]['confidence'] > 70:
            reminder_time = datetime.now() + timedelta(hours=hours_before)
            return {
                'reminder_set': True,
                'reminder_time': reminder_time.strftime('%I:%M %p'),
                'message': f"Reminder: You might need a {prediction[0]['scenario_type']} excuse soon.",
                'suggestion': prediction[0]['suggestion']
            }
        
        return {'reminder_set': False, 'message': 'No high-probability need detected.'}