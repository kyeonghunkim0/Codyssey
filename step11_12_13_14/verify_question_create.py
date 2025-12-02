import sys
import os

# Add the current directory to sys.path so we can import main
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from main import app
from database import SessionLocal
from models import Question

client = TestClient(app)

def verify_question_create():
    # 1. Create a question
    response = client.post(
        "/api/question/create",
        json={"subject": "Test Subject", "content": "Test Content"}
    )
    
    if response.status_code != 204:
        print(f"Failed to create question. Status code: {response.status_code}")
        print(response.json())
        sys.exit(1)
        
    print("Question created successfully (Status 204).")

    # 2. Verify it exists in the database
    db = SessionLocal()
    try:
        question = db.query(Question).filter(Question.subject == "Test Subject").first()
        if question:
            print(f"Verified in DB: {question.subject}, {question.content}")
        else:
            print("Failed to verify in DB.")
            sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    verify_question_create()
