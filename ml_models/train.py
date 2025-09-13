import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import json
import os
from ml_models.classifier import ResumeClassifier

def load_dataset(csv_path: str):
    """
    Load and prepare the dataset from CSV
    """
    df = pd.read_csv(csv_path)
    return df['text'].tolist(), df['category'].tolist()

def train_and_evaluate():
    """
    Train the model and evaluate its performance
    """
    # Load dataset
    csv_path = "data_storage/resume_dataset.csv"
    print("Loading dataset...")
    texts, labels = load_dataset(csv_path)
    
    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42
    )
    
    # Prepare training data in the format expected by ResumeClassifier
    training_data = [{"text": text, "category": label} for text, label in zip(X_train, y_train)]
    test_data = [{"text": text, "category": label} for text, label in zip(X_test, y_test)]
    
    # Initialize and train classifier
    print("Training classifier...")
    classifier = ResumeClassifier()
    classifier.train(training_data)
    
    # Evaluate on test set
    print("\nEvaluating model...")
    predictions = []
    for item in test_data:
        # Create a temporary file for testing
        temp_file = "data_storage/temp_test.txt"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(item["text"])
        try:
            pred = classifier.classify(temp_file)
            predictions.append(pred)
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    # Print classification report
    print("\nClassification Report:")
    print(classification_report(y_test, predictions))
    
    print("\nModel training and evaluation completed!")
    return classifier

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("data_storage/temp", exist_ok=True)
    os.makedirs("ml_models/trained_model", exist_ok=True)
    
    # Train and evaluate the model
    classifier = train_and_evaluate()
