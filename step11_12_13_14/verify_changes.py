import sys
import os
import contextlib
from sqlalchemy.orm import Session
from sqlalchemy import text

# Add the project directory to sys.path
sys.path.append('/Users/kimkyeonghun/Desktop/Codyssey/step11_12')

from database import get_db, SessionLocal
from domain.question.question_schema import Question as QuestionSchema
from models import Question as QuestionModel
import datetime
from pydantic import BaseModel

def test_get_db_context_manager():
    print("Testing get_db context manager...")
    try:
        with get_db() as db:
            print("  Database session acquired.")
            assert isinstance(db, Session)
            # Check if session is active (basic check)
            db.execute(text("SELECT 1"))
    except Exception as e:
        print(f"  FAILED: {e}")
        return False
    print("  Database session closed (implicitly by context manager).")
    print("  PASSED")
    return True

def test_schema_orm_mode():
    print("\nTesting Question schema orm_mode (from_attributes)...")
    # Create a dummy ORM object
    dummy_question = QuestionModel(
        id=1,
        subject="Test Subject",
        content="Test Content",
        create_date=datetime.datetime.now()
    )
    
    try:
        # Try to create a Pydantic model from the ORM object
        pydantic_question = QuestionSchema.model_validate(dummy_question)
        print(f"  Successfully created Pydantic model: {pydantic_question}")
        
        # Verify fields
        assert pydantic_question.id == dummy_question.id
        assert pydantic_question.subject == dummy_question.subject
        
        print("  PASSED")
        return True
    except Exception as e:
        print(f"  FAILED: {e}")
        return False

def test_bonus_orm_mode_false():
    print("\nTesting Bonus: from_attributes = False...")
    
    # Define a new class with from_attributes = False
    class QuestionSchemaFalse(BaseModel):
        id: int
        subject: str
        content: str
        create_date: datetime.datetime

        class Config:
            from_attributes = False
    
    dummy_question = QuestionModel(
        id=1,
        subject="Test Subject",
        content="Test Content",
        create_date=datetime.datetime.now()
    )
    
    try:
        QuestionSchemaFalse.model_validate(dummy_question)
        print("  FAILED: Should have raised an error with from_attributes=False")
        return False
    except Exception as e:
        print(f"  PASSED: Caught expected error: {e}")
    
    return True

if __name__ == "__main__":
    results = [
        test_get_db_context_manager(),
        test_schema_orm_mode(),
        test_bonus_orm_mode_false()
    ]
    
    if all(results):
        print("\nAll tests PASSED!")
        sys.exit(0)
    else:
        print("\nSome tests FAILED!")
        sys.exit(1)
