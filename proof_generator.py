from datetime import datetime, timedelta
import random
import json

class ProofGenerator:
    def __init__(self):
        self.proof_templates = self._init_templates()
    
    def _init_templates(self):
        return {
            "doctor_note": self._generate_doctor_note,
            "screenshot": self._generate_screenshot,
            "location_log": self._generate_location_log,
            "chat_message": self._generate_chat_message,
            "email_thread": self._generate_email_thread,
            "system_alert": self._generate_system_alert
        }
    
    def generate_proof(self, proof_type, scenario, custom_details=None):
        """Generate fake proof based on type"""
        if proof_type in self.proof_templates:
            return self.proof_templates[proof_type](scenario, custom_details)
        return self._generate_generic_proof(scenario)
    
    def _generate_doctor_note(self, scenario, details=None):
        """Generate a fake doctor's note"""
        doctors = ["Dr. Sarah Johnson", "Dr. Michael Chen", "Dr. Emily Rodriguez", "Dr. James Wilson"]
        conditions = {
            "migraine": "Acute migraine episode requiring rest",
            "stomach": "Gastrointestinal infection",
            "respiratory": "Upper respiratory infection",
            "injury": "Musculoskeletal strain",
            "fever": "Fever of unknown origin"
        }
        
        condition = random.choice(list(conditions.keys()))
        if details and "condition" in details:
            condition = details["condition"]
        
        note = f"""
╔══════════════════════════════════════════════════════════╗
║                    MEDICAL CERTIFICATE                    ║
╠══════════════════════════════════════════════════════════╣
║  Patient Name: [PATIENT NAME HERE]                        ║
║  Date: {datetime.now().strftime('%B %d, %Y')}              ║
║  Time: {datetime.now().strftime('%I:%M %p')}               ║
║                                                            ║
║  Diagnosis: {conditions[condition]}                        ║
║                                                            ║
║  Symptoms Reported:                                        ║
║  • {random.choice(['Fever', 'Nausea', 'Pain', 'Fatigue'])}                 ║
║  • {random.choice(['Dizziness', 'Cough', 'Headache', 'Weakness'])}          ║
║                                                            ║
║  Recommended Action:                                       ║
║  • Bed rest for {random.randint(24, 72)} hours                              ║
║  • Avoid work/school until symptoms subside               ║
║  • Follow up if symptoms persist                          ║
║                                                            ║
║  Physician Signature:                                      ║
║  {random.choice(doctors)}                                   ║
║  License #: {random.randint(10000, 99999)}                 ║
║                                                            ║
║  [THIS IS A GENERATED DOCUMENT FOR DEMO PURPOSES]         ║
╚══════════════════════════════════════════════════════════╝
"""
        return note
    
    def _generate_screenshot(self, scenario, details=None):
        """Generate a fake screenshot text representation"""
        current_time = datetime.now()
        
        if "late" in scenario.lower():
            screenshot = f"""
┌─────────────────────────────────────────────────────────┐
│  📱 SCREENSHOT - {current_time.strftime('%I:%M %p')}                    │
├─────────────────────────────────────────────────────────┤
│  [Google Maps]                                           │
│  ⚠️ ACCIDENT AHEAD - 45 min delay                       │
│  Your ETA: { (current_time + timedelta(minutes=45)).strftime('%I:%M %p') }    │
│                                                          │
│  Alternative route found? ❌ No                          │
│  Traffic: 🔴 Heavy congestion                            │
│                                                          │
├─────────────────────────────────────────────────────────┤
│  [Messages]                                              │
│  System: Service disruption in your area                │
│  Estimated resolution: 1-2 hours                        │
└─────────────────────────────────────────────────────────┘
"""
        elif "internet" in scenario.lower() or "online" in scenario.lower():
            screenshot = f"""
┌─────────────────────────────────────────────────────────┐
│  💻 SCREENSHOT - System Status                           │
├─────────────────────────────────────────────────────────┤
│  ISP Outage Report                                       │
│  • Status: ⚠️ Major Outage                               │
│  • Affected: Your area (postcode {random.randint(10000, 99999)})    │
│  • Started: {(current_time - timedelta(hours=1)).strftime('%I:%M %p')}        │
│  • ETA Fix: { (current_time + timedelta(hours=2)).strftime('%I:%M %p') }      │
│                                                          │
│  [Screenshot saved to gallery]                          │
└─────────────────────────────────────────────────────────┘
"""
        else:
            screenshot = f"""
┌─────────────────────────────────────────────────────────┐
│  📸 SCREENSHOT - {current_time.strftime('%Y-%m-%d %H:%M')}              │
├─────────────────────────────────────────────────────────┤
│  Notification: System Alert                             │
│  • {random.choice(['Technical difficulties', 'Service interruption', 'Maintenance ongoing'])}  │
│  • Reference ID: #{random.randint(1000, 9999)}          │
│  • Please check back later                              │
└─────────────────────────────────────────────────────────┘
"""
        return screenshot
    
    def _generate_location_log(self, scenario, details=None):
        """Generate fake location history"""
        now = datetime.now()
        locations = [
            ("Home", now - timedelta(hours=2)),
            ("En Route", now - timedelta(hours=1, minutes=30)),
            ("Stopped - Traffic", now - timedelta(hours=1)),
            ("Stopped - Incident", now - timedelta(minutes=30)),
            ("Current Location", now)
        ]
        
        log = "📍 LOCATION HISTORY LOG\n" + "="*40 + "\n"
        for location, time in locations:
            log += f"{time.strftime('%H:%M')} - {location}\n"
        
        if "traffic" in scenario.lower():
            log += f"\n🚗 Traffic Report: Heavy congestion - {random.randint(30, 90)} min delay\n"
            log += f"🔄 Alternative route: Not available\n"
        
        log += "\n[Generated location data - For demonstration only]"
        return log
    
    def _generate_chat_message(self, scenario, details=None):
        """Generate fake chat message screenshot"""
        senders = ["Mom", "Dad", "Partner", "Roommate", "Landlord"]
        sender = random.choice(senders)
        
        messages = f"""
┌─────────────────────────────────────────────────────────┐
│  💬 iMessage - {sender}                                   │
├─────────────────────────────────────────────────────────┤
│  [{sender} {datetime.now().strftime('%I:%M %p')}]:       │
│  Hey, everything okay? Saw you were rushing out         │
│                                                          │
│  [You {datetime.now().strftime('%I:%M %p')}]:            │
│  Not really, {random.choice(['car broke down', 'had an emergency', 'feeling really sick', 'got locked out'])}  │
│                                                          │
│  [{sender} {datetime.now().strftime('%I:%M %p')}]:       │
│  Oh no! Let me know if you need anything                │
│                                                          │
│  [You {datetime.now().strftime('%I:%M %p')}]:            │
│  Thanks, will update you soon                           │
└─────────────────────────────────────────────────────────┘
"""
        return messages
    
    def _generate_email_thread(self, scenario, details=None):
        """Generate fake email thread"""
        thread = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 EMAIL THREAD - System Notification
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

From: noreply@system-alerts.com
To: [USER_EMAIL]
Subject: Service Disruption Notice

Dear Customer,

We are experiencing technical difficulties affecting your area.
Ticket #{random.randint(10000, 99999)} has been created.

Estimated resolution time: 2-3 hours

We apologize for the inconvenience.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

From: support@provider.com
To: [USER_EMAIL]
Subject: RE: Service Disruption Notice

Update: Our team is actively working on the issue.
We will notify you once resolved.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return thread
    
    def _generate_system_alert(self, scenario, details=None):
        """Generate fake system alert"""
        alert = f"""
╔══════════════════════════════════════════════════════════╗
║  🚨 SYSTEM ALERT 🚨                                       ║
╠══════════════════════════════════════════════════════════╣
║  Priority: HIGH                                           ║
║  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}   ║
║  Alert ID: AL-{random.randint(1000, 9999)}                ║
║                                                            ║
║  Description:                                             ║
║  {random.choice(['Unexpected system maintenance', 'Security protocol triggered', 'Network interruption'])}  ║
║                                                            ║
║  Affected Services:                                       ║
║  • {random.choice(['Email', 'Calendar', 'VPN', 'All services'])}                    ║
║                                                            ║
║  Status: Investigating                                    ║
║  Next Update: { (datetime.now() + timedelta(minutes=30)).strftime('%I:%M %p') }      ║
╚══════════════════════════════════════════════════════════╝
"""
        return alert
    
    def _generate_generic_proof(self, scenario):
        """Fallback proof generator"""
        return f"""
[PROOF GENERATED FOR: {scenario.upper()}]
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Type: Documentation
Note: Supporting evidence for your situation
"""
    
    def get_proof_types(self):
        """Return available proof types"""
        return list(self.proof_templates.keys())

# Initialize proof generator
proof_gen = ProofGenerator()