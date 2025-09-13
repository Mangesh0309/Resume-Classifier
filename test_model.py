from ml_models.classifier import ResumeClassifier

def test_classifier(resume_path):
    # Initialize classifier
    classifier = ResumeClassifier()
    
    # Classify the resume
    try:
        prediction = classifier.classify(resume_path)
        print(f"\nPredicted category: {prediction}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_classifier("test_resume.txt")
