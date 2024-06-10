from app import db, User, History, Question
from datetime import datetime

def create_instances():
    # Create 3 User instances
    user1 = User(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password="password1",
        profession="Student",
        age=25,
        country="USA",
        state="California",
        city="Los Angeles",
        area_of_interest="Math",
        school="UCLA",
        school_id=101
    )

    user2 = User(
        first_name="Jane",
        last_name="Smith",
        email="jane.smith@example.com",
        password="password2",
        profession="Teacher",
        age=30,
        country="USA",
        state="New York",
        city="New York City",
        area_of_interest="Science",
        school="NYU",
        school_id=102
    )

    user3 = User(
        first_name="Alice",
        last_name="Johnson",
        email="alice.johnson@example.com",
        password="password3",
        profession="Others",
        age=28,
        country="Canada",
        state="Ontario",
        city="Toronto",
        area_of_interest="Art",
        school="UofT",
        school_id=103
    )

    # Add users to session
    db.session.add_all([user1, user2, user3])
    db.session.commit()

    # Create 3 History instances
    history1 = History(
        date_created=datetime.now(),
        category="Math",
        export_type="Download",
        quiz_count=5,
        user_mode="Student",
        user_id=user1.id,
        mcqs="Sample MCQs 1"
    )

    history2 = History(
        date_created=datetime.now(),
        category="Science",
        export_type="On-page",
        quiz_count=10,
        user_mode="Teacher",
        user_id=user2.id,
        mcqs="Sample MCQs 2"
    )

    history3 = History(
        date_created=datetime.now(),
        category="Art",
        export_type="Download",
        quiz_count=15,
        user_mode="Others",
        user_id=user3.id,
        mcqs="Sample MCQs 3"
    )

    # Add histories to session
    db.session.add_all([history1, history2, history3])
    db.session.commit()

    # Create 3 Question instances
    question1 = Question(
        date_created=datetime.now(),
        category="Math",
        quiz_count=5,
        user_id=user1.id,
        mcqs="Sample Question 1"
    )

    question2 = Question(
        date_created=datetime.now(),
        category="Science",
        quiz_count=10,
        user_id=user2.id,
        mcqs="Sample Question 2"
    )

    question3 = Question(
        date_created=datetime.now(),
        category="Art",
        quiz_count=15,
        user_id=user3.id,
        mcqs="Sample Question 3"
    )

    # Add questions to session
    db.session.add_all([question1, question2, question3])
    db.session.commit()

    print("Instances created successfully.")

if __name__ == "__main__":
  create_instances()
