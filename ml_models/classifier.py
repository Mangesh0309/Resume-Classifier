import os
import joblib
import json
from typing import Dict, List, Optional, Union
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from .text_extractor import extract_text_from_file
from .preprocessor import preprocess_text

class ResumeClassifier:
    def __init__(self, model_dir: str = "ml_models/trained_model"):
        self.model_dir = model_dir
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.model = MultinomialNB()
        self.is_trained = False
        self.load_model()

    def train(self, training_data: List[Dict[str, str]]):
        """
        Train the classifier with labeled resume data
        """
        texts = [item["text"] for item in training_data]
        labels = [item["category"] for item in training_data]
        
        # Preprocess texts
        processed_texts = [preprocess_text(text) for text in texts]
        
        # Create feature vectors
        X = self.vectorizer.fit_transform(processed_texts)
        y = np.array(labels)
        
        # Train the model
        self.model.fit(X, y)
        self.is_trained = True
        
        # Save the model
        self.save_model()

    def classify(self, input_data: Union[str, dict]) -> Dict[str, str]:
        """
        Classify a single resume and rate its quality
        input_data can be either a file path or the resume text directly
        """
        if not self.is_trained:
            raise ValueError("Model needs to be trained first!")
        
        # Get text from input
        if isinstance(input_data, str):
            if os.path.exists(input_data):
                text = extract_text_from_file(input_data)
            else:
                text = input_data
        else:
            text = input_data.get("text", "")
        
        # Preprocess the text
        processed_text = preprocess_text(text)
        
        # Transform text to feature vector
        X = self.vectorizer.transform([processed_text])
        
        # Make category prediction
        category = self.model.predict(X)[0]
        
        # Calculate quality score based on key factors
        quality_score = self._calculate_quality_score(text)
        
        return {
            "category": category,
            "quality": quality_score
        }

    def _calculate_quality_score(self, text: str) -> str:
        """
        Calculate a quality score for the resume based on various factors
        """
        score = 0
        text_lower = text.lower()
        
        # Key sections check (weighted by importance)
        sections = {
            'experience': 25,
            'education': 20,
            'skills': 15,
            'projects': 15,
            'achievements': 10,
            'summary': 5,
            'certifications': 10
        }
        
        for section, weight in sections.items():
            if section in text_lower:
                score += weight
        
        # Check for quantifiable achievements
        achievement_indicators = [
            r'\d+%',           # Percentages
            r'\d+ years',      # Years of experience
            r'increased',      # Impact words
            r'decreased',
            r'improved',
            r'led',
            r'managed',
            r'developed'
        ]
        
        for indicator in achievement_indicators:
            if any(word in text_lower for word in indicator.split('|')):
                score += 5
        
        # Convert score to quality rating
        if score >= 85:
            return "best"
        elif score >= 70:
            return "good"
        elif score >= 50:
            return "average"
        else:
            return "poor"

    def save_model(self):
        """
        Save the trained model and vectorizer
        """
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Save vectorizer
        joblib.dump(self.vectorizer, os.path.join(self.model_dir, "vectorizer.joblib"))
        
        # Save classifier
        joblib.dump(self.model, os.path.join(self.model_dir, "classifier.joblib"))
        
        # Save model information
        model_info = {
            "is_trained": self.is_trained,
            "categories": list(self.model.classes_) if self.is_trained else []
        }
        with open(os.path.join(self.model_dir, "model_info.json"), "w") as f:
            json.dump(model_info, f)

    def load_model(self):
        """
        Load the trained model and vectorizer if they exist
        """
        try:
            # Load model information
            with open(os.path.join(self.model_dir, "model_info.json"), "r") as f:
                model_info = json.load(f)
                self.is_trained = model_info["is_trained"]
            
            if self.is_trained:
                # Load vectorizer
                self.vectorizer = joblib.load(os.path.join(self.model_dir, "vectorizer.joblib"))
                
                # Load classifier
                self.model = joblib.load(os.path.join(self.model_dir, "classifier.joblib"))
                
        except FileNotFoundError:
            # Model files don't exist yet
            pass
