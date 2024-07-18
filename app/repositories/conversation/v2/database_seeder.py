import bcrypt
import json
from app.repositories.admin.users.user_repo import UserRepo
from app.repositories.conversation.v2.categories.category_repo import CategoryRepo
from app.repositories.conversation.v2.categories.sub_categories.sub_category_repo import SubCategoryRepo
from app.repositories.conversation.v2.categories.sub_categories.questions.question_repo import QuestionRepo
from app.repositories.conversation.v2.conversation_repo import ConversationRepo
from app.models.conversation.v2.categories.category import ConversationV2Category
from app.models.conversation.v2.categories.sub_categories.sub_category import ConversationV2CategoriesSubCategory
from app.models.conversation.v2.categories.sub_categories.questions.question import ConversationV2CategoriesSubCategoriesQuestion
from app.models.admin.users.user import AdminUser
from app.patterns.models.factory import ModelFactory
from app.patterns.models.adapter import ModelAdapter
from app.patterns.models.builder import ModelBuilder


def seeder_handler_with_factory(db):
    try:
        factory = ModelFactory()
        # Insert an admin user
        admin_user_data = {
            'username': 'admin_user',
            'email': 'adminuser@mail.com',
            'password': bcrypt.hashpw('adminuser@mail.com'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        }
        admin_user_instance = factory.create_instance(
            AdminUser, **admin_user_data)
        UserRepo.create(db, admin_user_instance)

        # Insert categories from JSON files
        filename = 'app/database/seeders/categories.json'
        with open(filename, 'r') as file:
            data = json.load(file)
            for cat in data:
                category_instance = factory.create_instance(
                    ConversationV2Category, **cat)
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
                sub_category_instance = factory.create_instance(
                    ConversationV2CategoriesSubCategory, **sub_cat_data)
                sub_category = SubCategoryRepo.create(
                    db, sub_category_instance)

                if 'questions' in sub_cat:
                    for quiz in sub_cat['questions']:
                        question_data = {
                            'category_id': sub_cat['category_id'],
                            'sub_category_id': sub_category.id,
                            'question': quiz['question'],
                            'marks': quiz['marks'],
                        }
                        question_instance = factory.create_instance(
                            ConversationV2CategoriesSubCategoriesQuestion, **question_data)
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


def seeder_handler_with_adapter(db):
    try:
        # Example: insert a dummy user with hashed password
        admin_user_data = {
            'username': 'admin_user',
            'email': 'adminuser@mail.com',
            'password': 'adminuser@mail.com'  # No need to hash here, adapter handles it
        }
        adapter = ModelAdapter(admin_user_data)
        admin_user_instance = adapter.adapt_admin_user()
        UserRepo.create(db, admin_user_instance)

        # Insert categories from JSON files
        filename = 'app/database/seeders/categories.json'
        with open(filename, 'r') as file:
            data = json.load(file)
            for cat in data:
                adapter = ModelAdapter(cat)
                category_instance = adapter.adapt_category()
                CategoryRepo.create(db, category_instance)

        # Insert subcategories and questions from JSON files
        filename = 'app/database/seeders/sub_categories.json'
        with open(filename, 'r') as file:
            data = json.load(file)
            for sub_cat in data:
                adapter = ModelAdapter(sub_cat)
                sub_category_instance = adapter.adapt_sub_category()
                sub_category = SubCategoryRepo.create(
                    db, sub_category_instance)

                if 'questions' in sub_cat:
                    for quiz in sub_cat['questions']:
                        adapter = ModelAdapter(
                            {**quiz, 'sub_category': sub_category.id})
                        question_instance = adapter.adapt_question()
                        QuestionRepo.create(db, question_instance)

        db.close()
        msg = "Database setup successful!"
        print(msg)
        return msg
    except Exception as e:
        msg = f"Error setting up database: {str(e)}"
        print(msg)
        return msg


def seeder_handler_with_builder(db):
    try:
        # Insert an admin user
        admin_user_data = {
            'username': 'admin_user',
            'email': 'adminuser@mail.com',
            'password': bcrypt.hashpw('adminuser@mail.com'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        }
        admin_user_builder = ModelBuilder(AdminUser)
        for key, value in admin_user_data.items():
            admin_user_builder.set_field(key, value)
        admin_user_instance = admin_user_builder.build()
        UserRepo.create(db, admin_user_instance)

        # Insert categories from JSON files
        filename = 'app/database/seeders/categories.json'
        with open(filename, 'r') as file:
            data = json.load(file)
            for cat in data:
                category_builder = ModelBuilder(ConversationV2Category)
                for key, value in cat.items():
                    category_builder.set_field(key, value)
                category_instance = category_builder.build()
                CategoryRepo.create(db, category_instance)

        # Insert subcategories and questions from JSON files
        filename = 'app/database/seeders/sub_categories.json'
        with open(filename, 'r') as file:
            data = json.load(file)
            for sub_cat in data:
                sub_cat_builder = ModelBuilder(
                    ConversationV2CategoriesSubCategory)
                sub_cat_builder.set_field('name', sub_cat['name'])
                sub_cat_builder.set_field(
                    'category_id', sub_cat['category_id'])
                sub_cat_builder.set_field(
                    'learn_instructions', sub_cat['learn_instructions']['content'])
                sub_category_instance = sub_cat_builder.build()
                sub_category = SubCategoryRepo.create(
                    db, sub_category_instance)

                if 'questions' in sub_cat:
                    for quiz in sub_cat['questions']:
                        question_builder = ModelBuilder(
                            ConversationV2CategoriesSubCategoriesQuestion)
                        question_builder.set_field(
                            'category_id', sub_cat['category_id'])
                        question_builder.set_field(
                            'sub_category_id', sub_category.id)
                        question_builder.set_field(
                            'question', quiz['question'])
                        question_builder.set_field('marks', quiz['marks'])
                        question_instance = question_builder.build()
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