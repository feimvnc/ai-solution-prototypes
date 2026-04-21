import ollama
import logging
import re

logger = logging.getLogger(__name__)

class OllamaTypingAssistant:
    def __init__(self, model="qwen2.5:3b"):
        self.model = model
        self.client = ollama.Client(host="http://localhost:11434")
    
    def check_connection(self):
        """Check if Ollama is running"""
        try:
            models = self.client.list()
            return True
        except Exception as e:
            logger.error(f"Ollama connection error: {str(e)}")
            return False
    
    def get_typing_tips(self, error_keys, wpm, accuracy):
        """Get personalized typing tips based on performance"""
        try:
            prompt = f"""As a typing tutor, provide 3 concise tips to improve typing skills based on:
- Common error keys: {', '.join(error_keys[:5]) if error_keys else 'None'}
- Current WPM: {wpm}
- Accuracy: {accuracy}%

Provide practical, actionable advice in 3 short bullet points."""

            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={'temperature': 0.7, 'num_predict': 150}
            )
            
            return response['response'].strip()
        except Exception as e:
            logger.error(f"Error getting typing tips: {str(e)}")
            return "Keep practicing! Focus on accuracy before speed."
    
    def generate_practice_text(self, difficulty="medium", focus_keys=None):
        """Generate custom practice text focusing on specific keys"""
        try:
            focus_str = f" focusing on keys: {', '.join(focus_keys)}" if focus_keys else ""
            
            prompt = f"""Generate a {difficulty} difficulty typing practice sentence (30-50 words){focus_str}. 
Make it interesting and grammatically correct. Only provide the sentence, no explanations."""

            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={'temperature': 0.8, 'num_predict': 100}
            )
            
            return response['response'].strip()
        except Exception as e:
            logger.error(f"Error generating practice text: {str(e)}")
            return "The quick brown fox jumps over the lazy dog."
    
    def analyze_typing_pattern(self, stats):
        """Analyze typing patterns and provide insights"""
        try:
            prompt = f"""Analyze this typing session:
- Total words: {stats.get('total_words', 0)}
- WPM: {stats.get('wpm', 0)}
- Accuracy: {stats.get('accuracy', 0)}%
- Time spent: {stats.get('time_spent', 0)} seconds

Provide a brief 2-sentence analysis and one specific improvement suggestion."""

            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={'temperature': 0.6, 'num_predict': 100}
            )
            
            return response['response'].strip()
        except Exception as e:
            logger.error(f"Error analyzing pattern: {str(e)}")
            return "Good effort! Keep practicing to improve your speed and accuracy."
    
    def translate_word(self, word):
        """Translate English word to Chinese"""
        try:
            prompt = f"""Translate the English word '{word}' to Chinese. 
Provide ONLY the Chinese translation, nothing else. No explanations, no pinyin, just the Chinese characters."""

            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={'temperature': 0.3, 'num_predict': 20}
            )
            
            translation = response['response'].strip()
            # Clean up any extra text, keep only Chinese characters
            import re
            chinese_only = re.findall(r'[\u4e00-\u9fff]+', translation)
            return chinese_only[0] if chinese_only else translation
        except Exception as e:
            logger.error(f"Error translating word: {str(e)}")
            return "译"
