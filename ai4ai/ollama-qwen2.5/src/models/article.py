from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Article:
    title: str
    url: str
    published_date: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None
    
    def to_dict(self):
        return {
            'title': self.title,
            'url': self.url,
            'published_date': self.published_date,
            'content': self.content,
            'summary': self.summary,
            'sentiment': self.sentiment,
            'sentiment_score': self.sentiment_score
        }
