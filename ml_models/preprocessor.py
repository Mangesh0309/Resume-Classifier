import re
from typing import List
import string

def preprocess_text(text: str) -> str:
    """
    Preprocess the text from a resume
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def extract_keywords(text: str) -> List[str]:
    """
    Extract important keywords from the text
    """
    # Add keyword extraction logic here
    # This is a placeholder implementation
    words = text.split()
    # Remove common words and keep only significant ones
    keywords = [word for word in words if len(word) > 3]
    return keywords
