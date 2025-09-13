from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict
import os
from ml_models.classifier import ResumeClassifier

app = FastAPI(title="Resume Classifier API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the classifier
classifier = ResumeClassifier()

@app.post("/classify")
async def classify_resume(file: UploadFile = File(...)) -> Dict:
    """
    Endpoint to classify a resume and rate its quality
    """
    # Save the uploaded file temporarily
    file_path = f"data_storage/temp/{file.filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    try:
        # Get classification result
        result = classifier.classify(file_path)
        return {
            "category": result["category"],
            "quality": result["quality"],
            "filename": file.filename
        }
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
