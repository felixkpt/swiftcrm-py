from app.models.users.user_model import User
from app.database.connection import SessionLocal

def seed_user():
    db = SessionLocal()
    try:
        default_email = "admin@example.com"

        existing_user = db.query(User).filter(User.email == default_email).first()
        if not existing_user:
            user = User(
                first_name="Admin",
                last_name="User",
                email=default_email,
                phone_number="1234567890",
                alternate_phone=None,
                password=default_email,
                status_id=1
            )
            db.add(user)
            db.commit()
            print("Default admin user seeded.")
        else:
            print("ℹAdmin user already exists, skipping.")

    except Exception as e:
        db.rollback()
        print(f"Error during user seeding: {e}")
    finally:
        db.close()
