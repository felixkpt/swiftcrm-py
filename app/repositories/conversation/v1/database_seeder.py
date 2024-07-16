import bcrypt  # Import bcrypt for password hashing
from app.database.old_connection import execute_insert
from app.repositories.conversation.v1.category import CategoryRepo as CatsRepo
from app.repositories.conversation.v1.sub_category import SubCategoryRepo as SubCatsRepo
from app.repositories.conversation.v1.conversation_repo import ConversationRepo


def setup_database(schema_file='app/database/schema.sql'):
    # insert_sub_categories_questions_from_json()
    # return

    # Execute the schema file to create tables
    # execute_schema(schema_file)

    # Insert dummy data or initial setup
    try:
        # Example: insert a dummy user with hashed password
        username = 'example_user'
        email = 'exampleuser@mail.com'
        plaintext_password = 'exampleuser@mail.com'

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(
            plaintext_password.encode('utf-8'), bcrypt.gensalt())

        # Insert into users table with hashed password
        execute_insert("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, hashed_password.decode('utf-8')))

        # Insert categories and subcategories from JSON files
        CatsRepo.insert_categories_from_json()
        SubCatsRepo.insert_sub_categories_from_json()
        SubCatsRepo.insert_sub_categories_questions_from_json()

        # Add a sample message
        ConversationRepo.add_message(
            1, 1, 1, 'user', 'Test message', '/conversation/v1/download-audio/sdiosdisdo.mp3')

        msg = "Database setup successful!"
        print(msg)
        return msg
    except Exception as e:
        msg = f"Error setting up database: {str(e)}"
        print(msg)
        return msg
