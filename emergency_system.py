from datetime import datetime
import random

class EmergencySystem:
    def __init__(self):
        self.emergency_types = {
            "technical": self._technical_emergency,
            "medical": self._medical_emergency,
            "family": self._family_emergency,
            "weather": self._weather_emergency,
            "transport": self._transport_emergency
        }
    
    def trigger_emergency(self, emergency_type, recipient, priority="high"):
        """Generate emergency message and call script"""
        if emergency_type in self.emergency_types:
            return self.emergency_types[emergency_type](recipient, priority)
        return self._generic_emergency(recipient, priority)
    
    def _technical_emergency(self, recipient, priority):
        issues = [
            "critical system failure",
            "data breach alert requiring immediate action",
            "server crash affecting all operations",
            "security incident requiring lockdown"
        ]
        issue = random.choice(issues)
        
        return {
            "type": "technical",
            "priority": priority,
            "text_message": f"⚠️ URGENT: {issue}. I need to handle this immediately. Will update you within the hour.",
            "call_script": f"Hello {recipient}, I'm dealing with a {issue} right now. I have to disconnect to handle this. I'll call you back as soon as it's resolved. Thank you for understanding.",
            "auto_response": f"Auto-reply: Currently handling a technical emergency. Will respond when available.",
            "estimated_duration": "30-60 minutes"
        }
    
    def _medical_emergency(self, recipient, priority):
        emergencies = [
            "sudden severe migraine with vision issues",
            "chest discomfort requiring immediate rest",
            "severe allergic reaction",
            "acute back pain - cannot move"
        ]
        emergency = random.choice(emergencies)
        
        return {
            "type": "medical",
            "priority": priority,
            "text_message": f"🚑 MEDICAL: {emergency}. Heading to urgent care. Will provide documentation.",
            "call_script": f"{recipient}, I need to go to urgent care right now - {emergency}. I'm really sorry but I have to go. I'll keep you posted.",
            "auto_response": f"Auto-reply: Medical emergency - unavailable at this time.",
            "estimated_duration": "2-4 hours"
        }
    
    def _family_emergency(self, recipient, priority):
        emergencies = [
            "family member had an accident",
            "child is sick and needs immediate care",
            "elderly parent needs emergency assistance",
            "family emergency requiring immediate attention"
        ]
        emergency = random.choice(emergencies)
        
        return {
            "type": "family",
            "priority": priority,
            "text_message": f"🏠 FAMILY EMERGENCY: {emergency}. Need to step away immediately.",
            "call_script": f"Hi {recipient}, there's a {emergency}. I have to go handle this right now. I'll explain more later. Thanks for understanding.",
            "auto_response": f"Auto-reply: Dealing with a family emergency. Will respond when possible.",
            "estimated_duration": "1-3 hours"
        }
    
    def _weather_emergency(self, recipient, priority):
        weather_events = [
            "severe thunderstorm warning in area",
            "flash flood alert on my route",
            "tornado watch - sheltering in place",
            "extreme heat advisory - advised not to travel"
        ]
        event = random.choice(weather_events)
        
        return {
            "type": "weather",
            "priority": "high",
            "text_message": f"🌩️ WEATHER ALERT: {event}. Cannot travel until conditions improve.",
            "call_script": f"{recipient}, there's a {event}. Emergency services are advising everyone to stay put. I'll update you when it clears.",
            "auto_response": f"Auto-reply: Unable to respond - severe weather conditions.",
            "estimated_duration": "1-2 hours"
        }
    
    def _transport_emergency(self, recipient, priority):
        transport_issues = [
            "accident blocking all lanes ahead",
            "vehicle breakdown on highway",
            "public transit shutdown due to incident",
            "road closure due to police activity"
        ]
        issue = random.choice(transport_issues)
        
        return {
            "type": "transport",
            "priority": priority,
            "text_message": f"🚗 TRANSPORT: {issue}. ETA unknown, will update when moving again.",
            "call_script": f"{recipient}, I'm stuck in {issue}. They're saying it could be a while. I'll let you know as soon as I'm moving again.",
            "auto_response": f"Auto-reply: Delayed due to transportation issues.",
            "estimated_duration": "45-90 minutes"
        }
    
    def _generic_emergency(self, recipient, priority):
        return {
            "type": "general",
            "priority": priority,
            "text_message": f"⚠️ EMERGENCY: Need to step away immediately. Will explain when possible.",
            "call_script": f"{recipient}, something urgent came up and I have to go. I'll reach out as soon as I can.",
            "auto_response": f"Auto-reply: Currently unavailable due to an emergency situation.",
            "estimated_duration": "Unknown"
        }
    
    def schedule_fake_call(self, recipient, delay_minutes=5):
        """Simulate scheduling a fake emergency call"""
        call_time = datetime.now()
        return {
            "scheduled": True,
            "recipient": recipient,
            "scheduled_time": call_time,
            "message": f"A fake emergency call has been scheduled to {recipient} in {delay_minutes} minutes.",
            "script": f"When the call connects, say: 'Hey {recipient}, sorry to interrupt but I just got an emergency call I need to take. Can I call you back?'"
        }
    
    def get_emergency_types(self):
        """Return available emergency types"""
        return list(self.emergency_types.keys())

# Create the instance that app.py expects
emergency = EmergencySystem()