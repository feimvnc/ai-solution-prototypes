import ollama
import logging
import re
from config.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaService:
    def __init__(self):
        self.model = Config.OLLAMA_MODEL
        self.client = ollama.Client(host=Config.OLLAMA_HOST)
    
    def check_connection(self) -> bool:
        """Check if Ollama is running and model is available"""
        try:
            models = self.client.list()
            model_names = [model['name'] for model in models.get('models', [])]
            logger.info(f"Available models: {model_names}")
            
            # Check if qwen2.5 is available (any version)
            qwen_available = any('qwen2.5' in name.lower() for name in model_names)
            
            if qwen_available:
                logger.info(f"Qwen2.5 model is available")
                return True
            else:
                logger.warning(f"Qwen2.5 model not found. Available: {model_names}")
                return False
                
        except Exception as e:
            logger.error(f"Error connecting to Ollama: {str(e)}")
            return False
    
    def summarize(self, text: str) -> str:
        """Summarize text using Qwen2.5"""
        if not text or len(text.strip()) < 50:
            return "Text too short to summarize."
        
        try:
            prompt = f"""Summarize the following financial news article in 2-3 concise sentences. Focus on the key facts and main points:

{text}

Summary:"""
            
            logger.info("Generating summary...")
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'temperature': 0.3,
                    'num_predict': 150
                }
            )
            
            summary = response['response'].strip()
            logger.info("Summary generated successfully")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return f"Error: {str(e)}"
    
    def analyze_sentiment(self, text: str) -> dict:
        """Analyze sentiment of text using Qwen2.5"""
        if not text or len(text.strip()) < 10:
            return {"sentiment": "neutral", "score": 0.0, "explanation": "Text too short"}
        
        try:
            prompt = f"""Analyze the sentiment of this financial news text. Respond with ONLY one word: positive, negative, or neutral.

Text: {text}

Sentiment:"""
            
            logger.info("Analyzing sentiment...")
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'temperature': 0.1,
                    'num_predict': 10
                }
            )
            
            sentiment_text = response['response'].strip().lower()
            
            # Extract sentiment
            if 'positive' in sentiment_text:
                sentiment = 'positive'
                score = 0.7
            elif 'negative' in sentiment_text:
                sentiment = 'negative'
                score = -0.7
            else:
                sentiment = 'neutral'
                score = 0.0
            
            logger.info(f"Sentiment: {sentiment} (score: {score})")
            
            return {
                "sentiment": sentiment,
                "score": score,
                "explanation": sentiment_text
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return {
                "sentiment": "error",
                "score": 0.0,
                "explanation": str(e)
            }
    
    def translate_to_chinese(self, text: str) -> str:
        """Translate text to Chinese using Qwen2.5"""
        if not text or len(text.strip()) < 5:
            return "文本太短，无法翻译。"
        
        try:
            prompt = f"""Please translate the following English text to Simplified Chinese. Only provide the translation, no explanations:

{text}

Chinese translation:"""
            
            logger.info("Translating to Chinese...")
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'temperature': 0.3,
                    'num_predict': 500
                }
            )
            
            translation = response['response'].strip()
            logger.info("Translation completed successfully")
            return translation
            
        except Exception as e:
            logger.error(f"Error translating text: {str(e)}")
            return f"翻译错误: {str(e)}"
