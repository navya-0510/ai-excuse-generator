from openai import OpenAI

class TranslationSystem:
    def __init__(self, base_url="http://localhost:11434/v1", model="llama3.2"):
        self.client = OpenAI(
            api_key="ollama",
            base_url=base_url
        )
        self.model = model
        
        self.languages = {
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'zh': 'Chinese (Simplified)',
            'ja': 'Japanese',
            'ko': 'Korean',
            'hi': 'Hindi',
            'ar': 'Arabic',
            'ru': 'Russian'
        }
    
    def translate_excuse(self, excuse_text, target_lang_code):
        """Translate an excuse to target language"""
        if target_lang_code not in self.languages:
            return {"error": f"Language {target_lang_code} not supported"}
        
        target_language = self.languages[target_lang_code]
        
        prompt = f"""Translate the following excuse to {target_language}.
        
Excuse: "{excuse_text}"

Rules:
1. Keep the same tone and urgency level
2. Make it sound natural in {target_language}
3. Preserve any specific details
4. Return ONLY the translated text, nothing else
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500
            )
            
            translated = response.choices[0].message.content.strip()
            
            return {
                'original': excuse_text,
                'translated': translated,
                'language': target_language,
                'language_code': target_lang_code
            }
        except Exception as e:
            return {
                'error': str(e),
                'original': excuse_text,
                'translated': excuse_text,
                'language': target_language
            }
    
    def translate_with_context(self, excuse_text, target_lang, context_type="work"):
        """Translate with context awareness for better accuracy"""
        context_notes = {
            "work": "Professional and formal tone required",
            "school": "Respectful academic tone",
            "social": "Casual and friendly tone",
            "family": "Warm and familiar tone"
        }
        
        prompt = f"""Translate this excuse to {self.languages.get(target_lang, target_lang)}.
Context: {context_notes.get(context_type, 'General')}

Original: "{excuse_text}"

Requirements:
- Match the cultural appropriateness for {self.languages.get(target_lang, target_lang)} speakers
- Maintain the original urgency level
- Sound natural and believable

Return ONLY the translation.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
        except:
            return excuse_text
    
    def get_supported_languages(self):
        """Return list of supported languages"""
        return self.languages
    
    def auto_detect_and_translate(self, excuse_text, target_lang):
        """Auto-detect source language and translate"""
        detect_prompt = f"What language is this text in? Answer with just the language name: {excuse_text[:100]}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": detect_prompt}],
                temperature=0,
                max_tokens=50
            )
            source_lang = response.choices[0].message.content.strip()
        except:
            source_lang = "Unknown"
        
        translation = self.translate_excuse(excuse_text, target_lang)
        translation['detected_source_language'] = source_lang
        
        return translation

# THIS LINE IS IMPORTANT - ADD IT AT THE END
translator = TranslationSystem()