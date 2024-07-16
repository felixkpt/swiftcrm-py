# app/repositories/conversation.py
from app.database.old_connection import execute_query, execute_insert
from datetime import datetime
from app.repositories.conversation.v1.sub_category import SubCategoryRepo
from app.repositories.conversation.v1.category import CategoryRepo
from app.services.helpers import filter_english_messages
import random
from app.repositories.conversation.v1.shared import SharedRepo

PROB_THRESHOLD_1 = 0.33
PROB_THRESHOLD_2 = 0.66

class ConversationRepo:
    @staticmethod
    def rate_question_answer(sub_cat_id, inserted_records):
        print('inserted_records::', inserted_records)
        return True

    @staticmethod
    def store_training_messages(sub_cat_id, my_info, assistant_info):
        request_message = my_info['message']
        response_message = assistant_info['message']

        user_id = 1
        cat_id = SubCategoryRepo.get_cat_id(sub_cat_id)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        created_at = now
        updated_at = now

        # Insert user's message
        user_message_query = """
        INSERT INTO conversation_v1_messages (user_id, category_id, sub_category_id, role, content, audio_uri, mode, created_at, updated_at)
        VALUES (%s, %s, %s, 'user', %s, %s, %s, %s, %s)
        """
        execute_insert(user_message_query, (user_id, cat_id, sub_cat_id,
                       request_message, my_info['audio_uri'], 'training', created_at, updated_at))

        # Insert assistant's response
        assistant_message_query = """
        INSERT INTO conversation_v1_messages (user_id, category_id, sub_category_id, role, content, audio_uri, mode, created_at, updated_at)
        VALUES (%s, %s, %s, 'assistant', %s, %s, %s, %s, %s)
        """
        execute_insert(assistant_message_query, (user_id, cat_id, sub_cat_id, response_message,
                       assistant_info['audio_uri'], 'training', created_at, updated_at))

        return {
            'results': ConversationRepo.fetch_inserted_records(sub_cat_id, user_id, cat_id, created_at),
            'metadata': {}
        }

    @staticmethod
    def store_interview_messages(sub_cat_id, my_info, assistant_info, interview_id):
        interview_question = SharedRepo.get_interview_question(sub_cat_id, user_id=1)
        current_interview_message = SharedRepo.get_current_interview_message(
            interview_id, role='user')

        interview_question['is_completed'] = interview_question['is_completed'] and interview_question[
            'last_question_id'] == current_interview_message['question_id']

        if interview_question['is_completed']:
            return {
                'results': [],
                'metadata': {
                    'question_number': interview_question['question_number'],
                    'is_completed': True
                }
            }

        request_message = my_info['message']
        response_message = assistant_info['message']

        user_id = 1
        cat_id = SubCategoryRepo.get_cat_id(sub_cat_id)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        created_at = now
        updated_at = now

        # Insert user's message
        message = SharedRepo.get_current_interview_message(interview_id, role='assistant')
        prev_question_id = message['question_id'] if message else None

        user_message_query = """
            INSERT INTO conversation_v1_messages (user_id, category_id, sub_category_id, role, mode, content, audio_uri, interview_id, question_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        execute_insert(user_message_query, (user_id, cat_id, sub_cat_id, 'user', 'interview', request_message,
                                            my_info['audio_uri'], interview_id, prev_question_id, created_at, updated_at))

        # Insert assistant's response
        session = SharedRepo.get_session_by_id(interview_id)
        print('interview_id:', interview_id, 'session', session)
        interview_id = session['id'] or None
        question_id = session['current_question_id'] or None

        assistant_message_query = """
        INSERT INTO conversation_v1_messages (user_id, category_id, sub_category_id, role, mode, content, audio_uri, interview_id, question_id, created_at, updated_at)
        VALUES (%s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s)
        """
        execute_insert(assistant_message_query, (user_id, cat_id, sub_cat_id, 'assistant', 'interview', response_message,
                                                 assistant_info['audio_uri'], interview_id, question_id, created_at, updated_at))

        interview_question = SharedRepo.get_interview_question(sub_cat_id, user_id=1)
        current_interview_message = SharedRepo.get_current_interview_message(
            interview_id, role='user')

        interview_question['is_completed'] = interview_question['is_completed'] and interview_question[
            'last_question_id'] == current_interview_message['question_id']

        return {
            'results': ConversationRepo.fetch_inserted_records(sub_cat_id, user_id, cat_id, created_at),
            'metadata': {
                'question_number': interview_question['question_number'],
                'is_completed': interview_question['is_completed']
            }
        }

    @staticmethod
    def store_messages(sub_cat_id, my_info, assistant_info, mode='training', interview_id=None):
        if mode == 'training':
            resp = ConversationRepo.store_training_messages(
                sub_cat_id, my_info, assistant_info)
        else:
            resp = ConversationRepo.store_interview_messages(
                sub_cat_id, my_info, assistant_info, interview_id)

        # Return the inserted records
        return resp

    @staticmethod
    def fetch_inserted_records(sub_cat_id, user_id, cat_id, created_at):
        query = """
        SELECT * FROM conversation_v1_messages
        WHERE user_id = %s AND category_id = %s AND sub_category_id = %s AND created_at = %s
        """
        return execute_query(query, (user_id, cat_id, sub_cat_id, created_at))

    @staticmethod
    def archive_messages(cat_id: int, sub_cat_id: int = None, mode='training'):
        if sub_cat_id:
            query = "UPDATE conversation_v1_messages SET status_id = 0 WHERE sub_category_id = %s AND mode = %s"
            execute_query(query, (sub_cat_id, mode))
        else:
            query = "UPDATE conversation_v1_messages SET status_id = 0 WHERE category_id = %s AND mode = %s"
            execute_query(query, (cat_id, mode))
        if mode == 'interview':
            query = "UPDATE conversation_v1_interviews SET status_id = 0 WHERE sub_category_id = %s"
            execute_query(query, (sub_cat_id,))

    @staticmethod
    def reset_messages(cat_id, sub_cat_id=None):
        if sub_cat_id:
            query = "DELETE FROM conversation_v1_messages WHERE sub_category_id = %s"
            execute_query(query, (sub_cat_id,))
        else:
            query = "DELETE FROM conversation_v1_messages WHERE category_id = %s"
            execute_query(query, (cat_id,))

    @staticmethod
    def add_message(user_id, cat_id, sub_cat_id, role, content, audio_uri, mode='training'):
        query = "INSERT INTO conversation_v1_messages (user_id, category_id, sub_category_id, role, content, audio_uri, mode) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (user_id, cat_id, sub_cat_id, role, content, audio_uri, mode)
        execute_insert(query, values)

    @staticmethod
    def get_training_instructions(sub_cat):
        learn_instructions = sub_cat['learn_instructions']

        instructions = [
            ' Your response will include some dry humor. Rate answer as fair, good or excellent accordingly.',
            ' Your response will include some step by step learn instructions. Rate answer as fair, good or excellent accordingly.',
            ' Your response will include an easy question. Rate answer as fair, good or excellent accordingly.',
            ' Your response will include a rather challenging question. Rate answer as fair, good or excellent accordingly.',
            ' Your response should be empathetic. Rate answer as fair, good or excellent accordingly.',
            ' Your response should include a motivational quote. Rate answer as fair, good or excellent accordingly.'
        ]

        probabilities = [PROB_THRESHOLD_1, PROB_THRESHOLD_2 -
                         PROB_THRESHOLD_1, 1 - PROB_THRESHOLD_2]

        x = random.uniform(0, 1)
        if x < probabilities[0]:
            add = instructions[0]
        elif x < probabilities[0] + probabilities[1]:
            add = instructions[1]
        else:
            add = instructions[2]

        return learn_instructions + add + ' Respond in English only.'

    @staticmethod
    def get_interview_instructions(sub_cat):
        cat_name = CategoryRepo.get_cat(sub_cat['category_id'])['name']
        learn_instructions = f'You are interviewing a user on "{cat_name} - {sub_cat["name"]}".'

        res = SharedRepo.get_interview_question(sub_cat['id'], user_id=1, update=True)
        question = res['question']
        question_number = res['question_number']
        is_completed = res['is_completed']
        interview_id = res['interview_id']

        if is_completed:
            learn_instructions = 'Interview completed. Thank the user! Tell them click the "Show My Results" button above. DO NOT ASK ANY QUESTION.'
        else:
            if question_number == 1:
                learn_instructions += f" Ask: {question} (This is question {question_number})."
            else:
                learn_instructions += f"Ask: {question} (This is question {question_number})."

        return learn_instructions + ' ASK THE QUESTION, DO NOT ANSWER. You MUST include question & number. eg "1. What is lorem ipsum?" Respond in English only. Keep your response under 40 words.', interview_id

    @staticmethod
    def get_recent_messages(sub_cat_id, mode='training'):
        sub_cat = SubCategoryRepo.get_sub_cat(sub_cat_id)
        if not sub_cat:
            raise ValueError(f"Invalid sub-category ID: {sub_cat_id}")

        interview_id = None
        if mode == 'training':
            learn_instructions = ConversationRepo.get_training_instructions(sub_cat)
        else:
            learn_instructions, interview_id = ConversationRepo.get_interview_instructions(sub_cat)

        messages = [{'content': learn_instructions, 'role': 'system'}]

        query = """
        SELECT content, role FROM conversation_v1_messages 
        WHERE sub_category_id = %s 
        AND mode = %s
        AND status_id = %s
        ORDER BY created_at DESC 
        LIMIT 20
        """
        recent_messages = execute_query(query, (sub_cat_id, mode, 1))

        limit = 0 if mode == 'interview' else 5

        english_messages = filter_english_messages(recent_messages, limit)

        messages.extend(reversed(english_messages))

        interview_id = interview_id
        return messages, interview_id
