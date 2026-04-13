from gtts import gTTS
import os
import tempfile
import platform
import subprocess
import time

class VoiceIntegration:
    def __init__(self):
        self.voice_enabled = True
    
    def text_to_speech(self, text, language='en', slow=False):
        """Convert text to speech and play it using Windows Media Player"""
        try:
            # Create temporary file for audio
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                temp_path = tmp_file.name
            
            # Generate speech using gTTS (requires internet)
            print("🔊 Generating speech...")
            tts = gTTS(text=text, lang=language, slow=slow)
            tts.save(temp_path)
            print(f"✅ Audio saved to: {temp_path}")
            
            # Play using Windows method
            self._play_audio_windows(temp_path)
            
            # Clean up
            try:
                os.unlink(temp_path)
            except:
                pass
            
            return True
        except Exception as e:
            print(f"❌ Voice error: {e}")
            print("💡 Make sure you have internet connection for gTTS")
            return False
    
    def _play_audio_windows(self, file_path):
        """Play audio using Windows Media Player"""
        try:
            # Method 1: Use Windows Media Player
            os.system(f'start wmplayer.exe "{file_path}"')
            print("🎵 Playing audio with Windows Media Player...")
            print("💡 Close the player window when done")
        except Exception as e:
            print(f"⚠️ Could not auto-play: {e}")
            print(f"📁 Audio file saved at: {file_path}")
            print("💡 You can play this file manually")
    
    def generate_voice_script(self, excuse_text):
        """Convert an excuse to a natural-sounding voice script"""
        voice_script = excuse_text.replace("I'm", "I am")
        voice_script = voice_script.replace("can't", "cannot")
        voice_script = voice_script.replace("don't", "do not")
        voice_script = voice_script.replace("won't", "will not")
        voice_script = voice_script.replace("I've", "I have")
        
        word_count = len(voice_script.split())
        estimated_seconds = word_count / 2.5
        
        return {
            'text': excuse_text,
            'voice_script': voice_script,
            'word_count': word_count,
            'estimated_duration_seconds': round(estimated_seconds, 1),
            'readable': voice_script
        }
    
    def create_phone_call_simulation(self, excuse_text, caller_name="You"):
        """Simulate a phone call script"""
        call_script = f"""
╔══════════════════════════════════════════════════════════════╗
║                    📞 PHONE CALL SIMULATION                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Caller: {caller_name}                                        ║
║  Recipient: [CONTACT NAME]                                    ║
║                                                               ║
║  [CALL CONNECTING...]                                         ║
║                                                               ║
║  YOU: "Hey, sorry to call suddenly but I need to explain..."  ║
║                                                               ║
║  {excuse_text}                                                ║
║                                                               ║
║  YOU: "I really appreciate you understanding. I'll make it    ║
║        up to you. Talk soon."                                 ║
║                                                               ║
║  [CALL ENDS - Duration: ~{len(excuse_text.split()) // 2} seconds]  ║
║                                                               ║
╚══════════════════════════════════════════════════════════════╝
"""
        return call_script
    
    def create_audio_file_only(self, text, filename="excuse_audio.mp3"):
        """Just create the audio file without playing"""
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(filename)
            print(f"✅ Audio saved to: {filename}")
            print(f"💡 You can play this file manually with any media player")
            return filename
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

# Initialize voice system
voice = VoiceIntegration()