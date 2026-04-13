from openai import OpenAI
import json
import re

class ExcuseGenerator:
    def __init__(self, base_url="http://localhost:11434/v1", model="llama3.2"):
        self.client = OpenAI(
            api_key="ollama",  # Can be any string for Ollama
            base_url=base_url
        )
        self.model = model
    
    def generate_excuse(self, scenario, context_type="work", urgency="medium", 
                        relationship="boss", additional_details=""):
        """
        Generate a context-aware excuse
        
        Parameters:
        - scenario: What happened (e.g., "late for meeting", "missed deadline")
        - context_type: work, school, social, family
        - urgency: low, medium, high
        - relationship: boss, professor, friend, parent
        - additional_details: Any extra info to include
        """
        
        # Context-specific prompts
        context_prompts = {
            "work": f"You are an employee who needs to explain {scenario} to your {relationship}. Make it professional but believable.",
            "school": f"You are a student explaining {scenario} to your {relationship}. Sound responsible and apologetic.",
            "social": f"You are canceling/explaining {scenario} to a {relationship}. Keep it casual but sincere.",
            "family": f"You are explaining {scenario} to your {relationship}. Sound respectful and honest."
        }
        
        # Urgency levels affect tone and drama
        urgency_tone = {
            "low": "Casual and brief explanation. Don't over-explain.",
            "medium": "Apologetic with reasonable explanation. Sound genuinely sorry.",
            "high": "Urgent and dramatic. Mention emergency-like circumstances. Show distress."
        }
        
        # Relationship affects formality
        relationship_formality = {
            "boss": "Very professional, respectful, solution-oriented",
            "professor": "Formal, respectful, academic",
            "friend": "Casual, honest, slightly self-deprecating",
            "parent": "Respectful, honest, remorseful"
        }
        
        system_prompt = f"""You are an AI excuse generator. Generate ONLY a valid JSON object, nothing else before or after.
        
        Your response must be exactly in this format:
        {{
            "excuse": "The complete excuse text here",
            "believability_score": 85,
            "suggested_proof": "Type of proof that would help (doctor_note/screenshot/location_log/chat/email)",
            "tone": "formal/casual/emotional",
            "estimated_length_seconds": 15
        }}
        
        Context: {context_prompts.get(context_type, context_prompts['work'])}
        Urgency: {urgency_tone.get(urgency, urgency_tone['medium'])}
        Relationship style: {relationship_formality.get(relationship, relationship_formality['friend'])}
        Additional details: {additional_details}
        
        Rules:
        1. Make excuses creative and not cliché (avoid "traffic" if possible)
        2. Match the tone to the relationship and urgency
        3. Keep excuse between 30-150 words
        4. Include specific details that sound real
        5. Believability score 0-100 based on how convincing it is
        """
        
        user_prompt = f"Generate a {urgency} urgency excuse for: {scenario}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content
            
            # Clean the response to extract JSON
            result_text = self._clean_json_response(result_text)
            
            # Parse JSON
            result = json.loads(result_text)
            
            # Ensure required fields exist
            if 'excuse' not in result:
                result['excuse'] = result_text[:200]
            if 'believability_score' not in result:
                result['believability_score'] = 75
            if 'suggested_proof' not in result:
                result['suggested_proof'] = 'none'
                
            return result
            
        except Exception as e:
            print(f"Error generating excuse: {e}")
            # Fallback response
            return {
                "excuse": f"I'm really sorry, but {self._get_fallback_excuse(scenario)}",
                "believability_score": 70,
                "suggested_proof": "text_message",
                "tone": "apologetic",
                "estimated_length_seconds": 10
            }
    
    def _clean_json_response(self, text):
        """Extract JSON from LLM response"""
        # Remove markdown code blocks
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        
        # Find JSON object
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json_match.group()
        return text
    
    def _get_fallback_excuse(self, scenario):
        """Fallback excuses if API fails"""
        fallbacks = {
            "late": "I encountered an unexpected situation on my way here.",
            "meeting": "I had a last-minute conflict that I couldn't reschedule.",
            "deadline": "I'm waiting on critical information to complete this.",
            "class": "I wasn't feeling well and didn't want to spread anything.",
        }
        
        for key, excuse in fallbacks.items():
            if key in scenario.lower():
                return excuse
        return "something unexpected came up that I need to handle urgently."
    
    def generate_multiple_excuses(self, scenario, context_type="work", count=3):
        """Generate multiple excuse options for the same scenario"""
        excuses = []
        urgency_levels = ["low", "medium", "high"]
        
        for i in range(min(count, len(urgency_levels))):
            excuse = self.generate_excuse(
                scenario, 
                context_type, 
                urgency_levels[i % len(urgency_levels)]
            )
            excuses.append(excuse)
        
        return excuses

# Initialize generator
generator = ExcuseGenerator()