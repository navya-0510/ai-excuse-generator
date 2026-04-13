from database import db
from excuse_generator import generator
from proof_generator import proof_gen
from emergency_system import emergency
from ranking_system import RankingSystem
from voice_integration import voice
from translation import translator
from scheduler import AutoScheduler
import json
from datetime import datetime

class ExcuseApp:
    def __init__(self):
        self.db = db
        self.generator = generator
        self.proof_gen = proof_gen
        self.emergency = emergency
        self.ranking_system = RankingSystem(db)
        self.voice = voice
        self.translator = translator
        self.scheduler = AutoScheduler(db)
        self.current_user = None
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print(" AI EXCUSE GENERATOR - COMPLETE SYSTEM ")
        print("="*60)
        print("\n📋 FEATURES:")
        print("1️⃣  Generate New Excuse")
        print("2️⃣  Generate Fake Proof")
        print("3️⃣  Emergency Alert System")
        print("4️⃣  Guilt-Tripping Apology")
        print("5️⃣  View History & Favorites")
        print("6️⃣  Smart Excuse Ranking")
        print("7️⃣  Auto-Schedule Prediction")
        print("8️⃣  Multi-Language Translation")
        print("9️⃣  Voice Integration")
        print("🔟  Compare Excuses")
        print("0️⃣  Exit")
        print("-"*60)
    
    def generate_excuse_flow(self):
        """Flow for generating an excuse"""
        print("\n EXCUSE GENERATION")
        print("-" * 30)
        
        scenario = input("📝 What happened? (e.g., 'late for work', 'missed meeting'): ")
        
        print("\n Context Type:")
        print("1. Work")
        print("2. School")
        print("3. Social")
        print("4. Family")
        context_choice = input("Choose (1-4): ")
        context_map = {"1": "work", "2": "school", "3": "social", "4": "family"}
        context_type = context_map.get(context_choice, "work")
        
        print("\n Urgency Level:")
        print("1. Low (casual)")
        print("2. Medium (apologetic)")
        print("3. High (urgent/emergency)")
        urgency_choice = input("Choose (1-3): ")
        urgency_map = {"1": "low", "2": "medium", "3": "high"}
        urgency = urgency_map.get(urgency_choice, "medium")
        
        print("\n Relationship:")
        print("1. Boss/Manager")
        print("2. Professor/Teacher")
        print("3. Friend")
        print("4. Parent")
        rel_choice = input("Choose (1-4): ")
        rel_map = {"1": "boss", "2": "professor", "3": "friend", "4": "parent"}
        relationship = rel_map.get(rel_choice, "friend")
        
        print("\n Generating excuse...")
        result = self.generator.generate_excuse(scenario, context_type, urgency, relationship)
        
        print("\n" + "="*50)
        print("✅ YOUR EXCUSE:")
        print("="*50)
        print(f"\n {result['excuse']}")
        print(f"\n Believability Score: {result['believability_score']}/100")
        print(f" Suggested Proof: {result['suggested_proof']}")
        print(f" Tone: {result.get('tone', 'apologetic')}")
        
        # Save to database
        excuse_id = self.db.save_excuse(scenario, context_type, urgency, relationship, 
                                        result['excuse'], result['believability_score'])
        
        # Record pattern for scheduling
        self.scheduler.record_usage(scenario, context_type)
        
        print(f"\n Saved to history (ID: {excuse_id})")
        
        # Ask for feedback
        feedback = input("\nWas this excuse successful? (y/n): ")
        if feedback.lower() == 'y':
            self.db.record_success(excuse_id, True)
            print(" Thanks for feedback! This will improve rankings.")
        
        return result
    
    def proof_generation_flow(self):
        """Flow for generating fake proof"""
        print("\n PROOF GENERATION")
        print("-" * 30)
        
        print("\nAvailable proof types:")
        proof_types = self.proof_gen.get_proof_types()
        for i, ptype in enumerate(proof_types, 1):
            print(f"{i}. {ptype.replace('_', ' ').title()}")
        
        choice = input(f"\nChoose (1-{len(proof_types)}): ")
        try:
            idx = int(choice) - 1
            proof_type = proof_types[idx]
        except:
            proof_type = "screenshot"
        
        scenario = input("What scenario is this proof for? ")
        
        print("\n Generating proof...")
        proof = self.proof_gen.generate_proof(proof_type, scenario)
        
        print("\n" + "="*50)
        print(" GENERATED PROOF:")
        print("="*50)
        print(proof)
        
        save = input("\nSave this proof? (y/n): ")
        if save.lower() == 'y':
            filename = f"proof_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(proof)
            print(f"Saved to {filename}")
    
    def emergency_flow(self):
        """Emergency alert flow"""
        print("\n EMERGENCY SYSTEM")
        print("-" * 30)
        
        print("\nEmergency types:")
        emergency_types = self.emergency.get_emergency_types()
        for i, etype in enumerate(emergency_types, 1):
            print(f"{i}. {etype.title()}")
        
        choice = input(f"\nChoose (1-{len(emergency_types)}): ")
        try:
            idx = int(choice) - 1
            emergency_type = emergency_types[idx]
        except:
            emergency_type = "technical"
        
        recipient = input("Who needs to be notified? ")
        priority = input("Priority (high/medium): ") or "high"
        
        alert = self.emergency.trigger_emergency(emergency_type, recipient, priority)
        
        print("\n" + "="*50)
        print(" EMERGENCY ALERT GENERATED:")
        print("="*50)
        print(f"\n TEXT MESSAGE:\n{alert['text_message']}")
        print(f"\n CALL SCRIPT:\n{alert['call_script']}")
        print(f"\n Estimated duration: {alert['estimated_duration']}")
        
        # Option to schedule fake call
        schedule = input("\nSchedule fake call reminder? (y/n): ")
        if schedule.lower() == 'y':
            call = self.emergency.schedule_fake_call(recipient)
            print(f"\n {call['message']}")
            print(f" Script: {call['script']}")
    
    def guilt_apology_flow(self):
        """Generate guilt-tripping apology"""
        print("\n GUILT-TRIPPING APOLOGY")
        print("-" * 30)
        
        offense = input("What did you do? (e.g., 'late', 'missed', 'forgot'): ")
        recipient = input("Who are you apologizing to? ")
        
        print("\nIntensity:")
        print("1. Low (brief, professional)")
        print("2. Medium (emotional)")
        print("3. High (dramatic, guilt-heavy)")
        intensity_choice = input("Choose (1-3): ")
        intensity_map = {"1": "low", "2": "medium", "3": "high"}
        intensity = intensity_map.get(intensity_choice, "medium")
        
        prompt = f"""Generate a {intensity} intensity guilt-tripping apology for being {offense} to {recipient}.
        Include: self-blame, acknowledgment of disappointment, promise to make up for it.
        Keep under 150 words. Make it sound genuinely remorseful."""
        
        response = self.generator.client.chat.completions.create(
            model=self.generator.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=300
        )
        
        apology = response.choices[0].message.content
        
        print("\n" + "="*50)
        print(" YOUR APOLOGY:")
        print("="*50)
        print(f"\n{apology}")
        
        # Option to voice it
        voice_option = input("\n Read aloud? (y/n): ")
        if voice_option.lower() == 'y':
            self.voice.text_to_speech(apology)
    
    def history_flow(self):
        """View history and favorites"""
        print("\n HISTORY & FAVORITES")
        print("-" * 30)
        
        print("1. View Recent History")
        print("2. View Favorites")
        print("3. Add to Favorites")
        print("4. Remove from Favorites")
        
        choice = input("Choose (1-4): ")
        
        if choice == "1":
            history = self.db.get_history(10)
            print("\n RECENT EXCUSES:")
            for item in history:
                fav = "⭐" if item['favorite'] else "  "
                print(f"\n{fav} [{item['id']}] {item['scenario']} - {item['context']}")
                print(f"    {item['excuse'][:100]}...")
                print(f"   📊 Used: {item['used']}x | Successful: {item['successful']}x")
        
        elif choice == "2":
            favs = self.db.get_favorites()
            print("\n FAVORITE EXCUSES:")
            for fav in favs:
                print(f"\n[{fav['id']}] {fav['scenario']} - {fav['context']}")
                print(f"    {fav['excuse'][:100]}...")
        
        elif choice == "3":
            excuse_id = input("Enter excuse ID to favorite: ")
            self.db.toggle_favorite(int(excuse_id))
            print(" Added to favorites!")
        
        elif choice == "4":
            excuse_id = input("Enter excuse ID to remove from favorites: ")
            self.db.toggle_favorite(int(excuse_id))
            print(" Removed from favorites!")
    
    def ranking_flow(self):
        """Show smart rankings"""
        print("\n SMART EXCUSE RANKING")
        print("-" * 30)
        
        scenario = input("Enter scenario to rank excuses for (or 'all'): ")
        
        if scenario.lower() == 'all':
            ranked = self.ranking_system.rank_excuses("", limit=10)
        else:
            ranked = self.ranking_system.rank_excuses(scenario, limit=10)
        
        if ranked:
            print("\n RANKINGS:")
            print("="*50)
            for excuse in ranked:
                print(f"\n#{excuse['rank']} - Score: {excuse['score']}/100")
                print(f"    {excuse['excuse'][:150]}...")
                print(f"   ✅ Success Rate: {excuse['success_rate']}%")
                print(f"    Believability: {excuse['believability']}/100")
                print(f"    Used: {excuse['times_used']} times")
        else:
            print("No data yet. Generate some excuses first!")
    
    def scheduler_flow(self):
        """Auto-schedule predictions"""
        print("\n AUTO-SCHEDULE PREDICTIONS")
        print("-" * 30)
        
        print("1. Predict next need")
        print("2. View peak excuse times")
        print("3. View weekly pattern")
        
        choice = input("Choose (1-3): ")
        
        if choice == "1":
            predictions = self.scheduler.predict_next_need()
            if predictions:
                print("\n🔮 PREDICTIONS:")
                for pred in predictions:
                    print(f"\n {pred['scenario_type'].title()} - {pred['confidence']}% confidence")
                    print(f"    {pred['suggestion']}")
            else:
                print("Not enough data yet. Keep using the app!")
        
        elif choice == "2":
            peaks = self.scheduler.get_peak_excuse_times()
            print("\n PEAK EXCUSE TIMES:")
            for peak in peaks:
                print(f"\n {peak['day']} at {peak['hour']}")
                print(f"   Frequency: {peak['frequency']} times")
                print(f"    {peak['suggestion']}")
        
        elif choice == "3":
            pattern = self.scheduler.get_weekly_pattern()
            print("\n WEEKLY PATTERN:")
            for day in pattern:
                bar = "█" * min(day['total_excuses'], 20)
                print(f"{day['day']:12} {bar} ({day['total_excuses']} excuses) - {day['risk_level']} risk")
    
    def translation_flow(self):
        """Multi-language translation"""
        print("\n MULTI-LANGUAGE TRANSLATION")
        print("-" * 30)
        
        excuse = input("Enter excuse to translate: ")
        
        print("\nSupported languages:")
        langs = self.translator.get_supported_languages()
        for code, name in list(langs.items())[:10]:
            print(f"  {code} - {name}")
        
        target = input("\nEnter language code (e.g., 'es' for Spanish): ")
        
        result = self.translator.translate_excuse(excuse, target)
        
        print("\n" + "="*50)
        print(f" Original: {result['original']}")
        print(f" Translated ({result['language']}): {result['translated']}")
        
        if 'detected_source_language' in result:
            print(f" Detected source: {result['detected_source_language']}")
    
    def voice_flow(self):
        """Voice integration"""
        print("\n VOICE INTEGRATION")
        print("-" * 30)
        
        print("1. Read excuse aloud")
        print("2. Generate phone call script")
        print("3. Create voice-ready script")
        
        choice = input("Choose (1-3): ")
        
        if choice == "1":
            excuse = input("Enter excuse text: ")
            print("\n Speaking...")
            self.voice.text_to_speech(excuse)
        
        elif choice == "2":
            excuse = input("Enter excuse for phone call: ")
            caller = input("Caller name (optional): ") or "You"
            script = self.voice.create_phone_call_simulation(excuse, caller)
            print(script)
        
        elif choice == "3":
            excuse = input("Enter excuse text: ")
            script = self.voice.generate_voice_script(excuse)
            print(f"\n Voice Script:\n{script['voice_script']}")
            print(f"\n⏱ Estimated duration: {script['estimated_duration_seconds']} seconds")
    
    def compare_flow(self):
        """Compare two excuses"""
        print("\n COMPARE EXCUSES")
        print("-" * 30)
        
        id1 = input("Enter first excuse ID: ")
        id2 = input("Enter second excuse ID: ")
        
        comparison = self.ranking_system.compare_excuses(int(id1), int(id2))
        
        if comparison:
            print("\n" + "="*50)
            print("EXCUSE 1:")
            print(f" {comparison['excuse1']['text'][:200]}...")
            print(f"✅ Success Rate: {comparison['excuse1']['success_rate']}%")
            print(f" Believability: {comparison['excuse1']['believability']}")
            
            print("\nEXCUSE 2:")
            print(f" {comparison['excuse2']['text'][:200]}...")
            print(f"✅ Success Rate: {comparison['excuse2']['success_rate']}%")
            print(f" Believability: {comparison['excuse2']['believability']}")
            
            print(f"\n VERDICT: {comparison['verdict']}")
        else:
            print("Invalid excuse IDs!")
    
    def run(self):
        """Run the main application"""
        print("\n Welcome to AI Excuse Generator!")
        print("Make sure Ollama is running with: ollama serve")
        
        while True:
            self.display_menu()
            choice = input("\n Select option: ")
            
            if choice == "1":
                self.generate_excuse_flow()
            elif choice == "2":
                self.proof_generation_flow()
            elif choice == "3":
                self.emergency_flow()
            elif choice == "4":
                self.guilt_apology_flow()
            elif choice == "5":
                self.history_flow()
            elif choice == "6":
                self.ranking_flow()
            elif choice == "7":
                self.scheduler_flow()
            elif choice == "8":
                self.translation_flow()
            elif choice == "9":
                self.voice_flow()
            elif choice == "10":
                self.compare_flow()
            elif choice == "0":
                print("\n Goodbye! Excuses ready when you need them!")
                break
            else:
                print(" Invalid option. Try again.")
            
            input("\nPress Enter to continue...")

# Run the app
if __name__ == "__main__":
    app = ExcuseApp()
    app.run()