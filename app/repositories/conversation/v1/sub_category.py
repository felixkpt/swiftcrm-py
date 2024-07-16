# app/models/subcategory.py
from typing import Dict, Any, List
from app.requests.schemas.conversation.v1.sub_category import QuestionRequest
from app.database.old_connection import execute_query, execute_insert
from app.repositories.conversation.v1.category import CategoryRepo
import json

class SubCategoryRepo:

    @staticmethod
    def sub_category_exists(category_id: int, sub_cat_name: str) -> bool:
        query = "SELECT 1 FROM conversation_v1_sub_categories WHERE category_id = %s AND name = %s"
        result = execute_query(query, (category_id, sub_cat_name))
        return len(result) > 0

    @staticmethod
    def add_sub_category(category_id: int, name: str, slug: str, learn_instructions: str):
        query = "INSERT INTO conversation_v1_sub_categories (category_id, name, slug, learn_instructions) VALUES (%s, %s, %s, %s)"
        execute_insert(query, (category_id, name, slug, learn_instructions))

    @staticmethod
    def update_sub_category(sub_category_id: int, sub_category: str):
        query = "UPDATE conversation_v1_sub_categories SET name = %s, slug = %s, learn_instructions = %s WHERE id = %s"
        execute_query(query, (sub_category.name, sub_category.slug, sub_category.learn_instructions, sub_category_id))

    @staticmethod
    def add_question_to_sub_category(sub_cat_id: int, question: QuestionRequest):
        query = "INSERT INTO conversation_v1_questions (sub_category_id, question, marks) VALUES (%s, %s, %s)"
        execute_insert(query, (sub_cat_id, question.question, question.marks))

    @staticmethod
    def add_questions_to_sub_category(sub_cat_id: int, questions: List[QuestionRequest]):
        for question in questions:
            SubCategoryRepo.add_question_to_sub_category(sub_cat_id, question)

    @staticmethod
    def get_sub_cats(cat_id: int) -> Dict[str, Any]:
        query = "SELECT * FROM conversation_v1_sub_categories WHERE category_id = %s AND status_id = %s"
        results = execute_query(query, (cat_id, 1))

        metadata = {
            'title': '{} Sub-categories list'.format(CategoryRepo.get_cat(cat_id)['name']) if results else None,
            'total_count': len(results) if results else 0
        }

        response = {
            'results': results,
            'metadata': metadata
        }

        return response

    @staticmethod
    def get_sub_cat(sub_cat_id):
        query = "SELECT * FROM conversation_v1_sub_categories WHERE id = %s and status_id = %s"
        result = execute_query(query, (sub_cat_id, 1))
        return result[0] if result else False

    @staticmethod
    def get_sub_cat_by_slug(sub_cat_slug):
        query = "SELECT * FROM conversation_v1_sub_categories WHERE slug = %s and status_id = %s"
        result = execute_query(query, (sub_cat_slug, 1))
        return result[0] if result else False

    @staticmethod
    def get_cat_id(sub_cat_id):
        sub_cat = SubCategoryRepo.get_sub_cat(sub_cat_id)
        return sub_cat['category_id'] if sub_cat else None

    @staticmethod
    def get_sub_cat_questions(sub_cat_id):
        query = "SELECT * FROM conversation_v1_questions WHERE sub_category_id = %s and status_id = %s"
        results = execute_query(query, (sub_cat_id, 1))

        metadata = {
            'title': '{} conversation_v1_questions list'.format(SubCategoryRepo.get_sub_cat(sub_cat_id)['name']) if results else None,
            'total_count': len(results) if results else 0
        }

        response = {
            'results': results,
            'metadata': metadata
        }

        return response

    @staticmethod
    def get_question(question_id):
        query = "SELECT * FROM conversation_v1_questions WHERE id = %s and status_id = %s"
        result = execute_query(query, (question_id, 1))
        return result[0] if result else False

    @staticmethod
    def question_exists(sub_category_id: int, sub_cat_name: str) -> bool:
        query = "SELECT 1 FROM conversation_v1_questions WHERE sub_category_id = %s AND question = %s"
        result = execute_query(query, (sub_category_id, sub_cat_name))
        return len(result) > 0

    @staticmethod
    def update_question(sub_category_id: int, question: QuestionRequest):
        query = "UPDATE conversation_v1_questions SET question = %s, marks = %s WHERE id = %s"
        execute_query(query, (question.question, question.marks, sub_category_id))

    @staticmethod
    def insert_sub_categories_from_json():
        filename = 'app/database/seeders/sub_categories.json'
        with open(filename, 'r') as file:
            data = json.load(file)

        for sub_cat in data:
            category_id = sub_cat['category_id']
            name = sub_cat['name']
            slug = sub_cat['slug']
            learn_instructions = sub_cat['learn_instructions']['content']

            sql = "INSERT INTO conversation_v1_sub_categories (category_id, name, slug, learn_instructions) VALUES (%s, %s, %s, %s)"
            values = (category_id, name, slug, learn_instructions)
            execute_insert(sql, values)

    @staticmethod
    def insert_sub_categories_questions_from_json():
        filename = 'app/database/seeders/sub_categories.json'
        with open(filename, 'r') as file:
            data = json.load(file)

        for sub_cat in data:
            if 'questions' in sub_cat:
                slug = sub_cat['slug']
                sub_category = SubCategoryRepo.get_sub_cat_by_slug(slug)
                if sub_category:
                    sub_category_id = sub_category['id']
                    for quiz in sub_cat['questions']:
                        question = quiz['question']
                        marks = quiz['marks']

                        sql_insert_question = "INSERT INTO conversation_v1_questions (sub_category_id, question, marks) VALUES (%s, %s, %s)"
                        values_insert_question = (sub_category_id, question, marks)
                        execute_insert(sql_insert_question, values_insert_question)
