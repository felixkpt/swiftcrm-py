import bcrypt
import json
from app.database.old_connection import execute_insert
from app.repositories.admin.users.user_repo import UserRepo
from app.repositories.conversation.v2.categories.category_repo import CategoryRepo
from app.repositories.conversation.v2.categories.sub_categories.sub_category_repo import SubCategoryRepo
from app.repositories.conversation.v2.categories.sub_categories.questions.question_repo import QuestionRepo
from app.repositories.conversation.v2.conversation_repo import ConversationRepo
from app.models.conversation.v2.categories.category import ConversationV2Category
from app.models.conversation.v2.categories.sub_categories.sub_category import ConversationV2CategoriesSubCategory
from app.models.conversation.v2.categories.sub_categories.questions.question import ConversationV2CategoriesSubCategoriesQuestion
from app.models.admin.users.user import AdminUser

class ModelAdapter:
    @staticmethod
    def adapt(model_class, data):
        return model_class(**data)

def seeder_handler(db):
    try:

        # Example: insert a dummy user with hashed password
        # Insert an admin user
        admin_user_data = {
            'username': 'admin_user',
            'email': 'adminuser@mail.com',
            'password': bcrypt.hashpw('adminuser@mail.com'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        }
        admin_user_instance = ModelAdapter.adapt(AdminUser, admin_user_data)
        UserRepo.create(db, admin_user_instance)

        # Insert categories from JSON files
        filename = 'app/database/seeders/categories.json'
        with open(filename, 'r') as file:
            data = json.load(file)
            for cat in data:
                category_instance = ModelAdapter.adapt(ConversationV2Category, cat)
                CategoryRepo.create(db, category_instance)

        # Insert subcategories and questions from JSON files
        filename = 'app/database/seeders/sub_categories.json'
        with open(filename, 'r') as file:
            data = json.load(file)
            for sub_cat in data:
                sub_cat_data = {
                    'name': sub_cat['name'],
                    'category_id': sub_cat['category_id'],
                    'learn_instructions': sub_cat['learn_instructions']['content'],
                }
                sub_category_instance = ModelAdapter.adapt(ConversationV2CategoriesSubCategory, sub_cat_data)
                sub_category = SubCategoryRepo.create(db, sub_category_instance)

                if 'questions' in sub_cat:
                    for quiz in sub_cat['questions']:
                        question_data = {
                            'category_id': sub_cat['category_id'],
                            'sub_category_id': sub_category.id,
                            'question': quiz['question'],
                            'marks': quiz['marks'],
                        }
                        question_instance = ModelAdapter.adapt(ConversationV2CategoriesSubCategoriesQuestion, question_data)
                        QuestionRepo.create(db, question_instance)

        # Add a sample message
        ConversationRepo.add_message(
            1, 1, 1, 'user', 'Test message', '/conversation/v1/download-audio/sdiosdisdo.mp3')

        db.close()
        msg = "Database setup successful!"
        print(msg)
        return msg
    except Exception as e:
        msg = f"Error setting up database: {str(e)}"
        print(msg)
        return msg
