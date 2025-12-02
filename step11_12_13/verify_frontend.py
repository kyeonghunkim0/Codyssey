import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def verify_frontend():
    response = client.get("/create_question.html")
    if response.status_code == 200:
        print("Frontend file served successfully.")
    else:
        print(f"Failed to serve frontend file. Status code: {response.status_code}")
        sys.exit(1)

if __name__ == "__main__":
    verify_frontend()
