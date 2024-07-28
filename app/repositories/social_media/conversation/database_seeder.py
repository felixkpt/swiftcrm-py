import bcrypt
import json
from app.repositories.users.user_repo import UserRepo
from app.repositories.social_media.conversation.categories.category_repo import CategoryRepo
from app.repositories.social_media.conversation.categories.sub_categories.sub_category_repo import SubCategoryRepo
from app.repositories.social_media.conversation.categories.sub_categories.questions.question_repo import QuestionRepo
from app.repositories.social_media.conversation.conversation_repo import ConversationRepo
from app.models.social_media.conversation.categories.category_model import SocialMediaConversationCategory as CategoryModel
from app.models.social_media.conversation.categories.sub_categories.sub_category_model import SocialMediaConversationCategoriesSubCategory as SubCategoryModel
from app.models.social_media.conversation.categories.sub_categories.questions.question_model import Soc4eiaConversationCategoriesSubCategoriesQuestion as QuestionModel
from app.models.users.user_model import User as UserModel
from app.patterns.models.factory import ModelFactory
from app.patterns.models.adapter import ModelAdapter
from app.patterns.models.builder import ModelBuilder

# Instantiating respective model repository classes
userRepo = UserRepo()
categoryRepo = CategoryRepo()
subCategoryRepo = SubCategoryRepo()
questionRepo = QuestionRepo()
conversationRepo = ConversationRepo()


async def user_seeder(db):
    try:
        # Insert an admin user
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'adminuser@mail.com',
            'phone_number': '+254712345678',
            'password': bcrypt.hashpw('adminuser@mail.com'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            'password_confirmation': bcrypt.hashpw('adminuser@mail.com'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        }
        user_builder = ModelBuilder(UserModel)
        for key, value in user_data.items():
            user_builder.set_field(key, value)
        user_instance = user_builder.build()
        await userRepo.create(db, user_instance)
    except Exception as e:
        msg = f"Error setting up user: {str(e)}"
        print(msg)
        return msg


async def categories_seeder(db):
    try:
        filename = 'app/database/seeders/categories.json'
        with open(filename, 'r') as file:
            data = json.load(file)
            for cat in data:
                category_builder = ModelBuilder(CategoryModel)
                for key, value in cat.items():
                    category_builder.set_field(key, value)
                category_instance = category_builder.build()
                await categoryRepo.create(db, category_instance)

    except Exception as e:
        msg = f"Error setting up categories: {str(e)}"
        print(msg)
        return msg


async def subcategories_seeder(db):
    try:
        filename = 'app/database/seeders/sub_categories.json'
        with open(filename, 'r') as file:
            data = json.load(file)
            for sub_cat in data:
                sub_cat_builder = ModelBuilder(
                    SubCategoryModel)
                sub_cat_builder.set_field('name', sub_cat['name'])
                sub_cat_builder.set_field(
                    'category_id', sub_cat['category_id'])
                sub_cat_builder.set_field(
                    'learn_instructions', sub_cat['learn_instructions']['content'])
                sub_category_instance = sub_cat_builder.build()
                sub_category = await subCategoryRepo.create(
                    db, sub_category_instance)

                if 'questions' in sub_cat:
                    for quiz in sub_cat['questions']:
                        question_builder = ModelBuilder(
                            QuestionModel)
                        question_builder.set_field(
                            'category_id', sub_cat['category_id'])
                        question_builder.set_field(
                            'sub_category_id', sub_category.id)
                        question_builder.set_field(
                            'question', quiz['question'])
                        question_builder.set_field('marks', quiz['marks'])
                        question_instance = question_builder.build()
                        await questionRepo.create(db, question_instance)

    except Exception as e:
        msg = f"Error setting up subcategories: {str(e)}"
        print(msg)
        return msg


async def seeder_handler_with_builder(db):
    try:
        # Insert a user
        await user_seeder(db)

        # Insert categories from JSON files
        await categories_seeder(db)

        # Insert subcategories and questions from JSON files
        await subcategories_seeder(db)

        # Add a sample message
        conversationRepo.add_message(
            1, 1, 1, 'user', 'Test message', '/conversation/v1/download-audio/sdiosdisdo.mp3')

        db.close()
        msg = "Database setup successful!"
        print(msg)
        return msg
    except Exception as e:
        msg = f"Error setting up database: {str(e)}"
        print(msg)
        return msg


async def seeder_handler_with_factory(db):
    try:
        factory = ModelFactory()
        # Insert an admin user
        user_data = {
            'username': 'user',
            'email': 'adminuser@mail.com',
            'password': bcrypt.hashpw('adminuser@mail.com'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        }
        user_instance = factory.create_instance(
            UserModel, **user_data)
        await userRepo.create(db, user_instance)

        # Insert categories from JSON files
        filename = 'app/database/seeders/categories.json'
        with open(filename, 'r') as file:
            data = json.load(file)
            for cat in data:
                category_instance = factory.create_instance(
                    CategoryModel, **cat)
                await categoryRepo.create(db, category_instance)

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
                    SubCategoryModel, **sub_cat_data)
                sub_category = await subCategoryRepo.create(
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
                            QuestionModel, **question_data)
                        await questionRepo.create(db, question_instance)

        # Add a sample message
        conversationRepo.add_message(
            1, 1, 1, 'user', 'Test message', '/conversation/v1/download-audio/sdiosdisdo.mp3')

        db.close()
        msg = "Database setup successful!"
        print(msg)
        return msg
    except Exception as e:
        msg = f"Error setting up database: {str(e)}"
        print(msg)
        return msg


async def seeder_handler_with_adapter(db):
    try:
        # Example: insert a dummy user with hashed password
        user_data = {
            'username': 'user',
            'email': 'adminuser@mail.com',
            'password': 'adminuser@mail.com'  # No need to hash here, adapter handles it
        }
        adapter = ModelAdapter(user_data)
        user_instance = adapter.adapt_user()
        await userRepo.create(db, user_instance)

        # Insert categories from JSON files
        filename = 'app/database/seeders/categories.json'
        with open(filename, 'r') as file:
            data = json.load(file)
            for cat in data:
                adapter = ModelAdapter(cat)
                category_instance = adapter.adapt_category()
                await categoryRepo.create(db, category_instance)

        # Insert subcategories and questions from JSON files
        filename = 'app/database/seeders/sub_categories.json'
        with open(filename, 'r') as file:
            data = json.load(file)
            for sub_cat in data:
                adapter = ModelAdapter(sub_cat)
                sub_category_instance = adapter.adapt_sub_category()
                sub_category = await subCategoryRepo.create(
                    db, sub_category_instance)

                if 'questions' in sub_cat:
                    for quiz in sub_cat['questions']:
                        adapter = ModelAdapter(
                            {**quiz, 'sub_category': sub_category.id})
                        question_instance = adapter.adapt_question()
                        await questionRepo.create(db, question_instance)

        db.close()
        msg = "Database setup successful!"
        print(msg)
        return msg
    except Exception as e:
        msg = f"Error setting up database: {str(e)}"
        print(msg)
        return msg
