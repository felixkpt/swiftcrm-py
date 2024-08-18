from datetime import datetime
from fastapi import Request, Depends
from sqlalchemy.exc import IntegrityError
from app.database.old_connection import execute_query, execute_insert
from app.repositories.social_media.conversation.categories.sub_categories.sub_category_repo import SubCategoryRepo
from app.repositories.social_media.conversation.categories.category_repo import CategoryRepo
from app.services.helpers import filter_english_messages
import random
from app.repositories.social_media.conversation.shared import SharedRepo

PROB_THRESHOLD_1 = 0.33
PROB_THRESHOLD_2 = 0.66


class ConversationRepo:
    @staticmethod
    def rate_question_answer(sub_cat_id, inserted_records):
        print('inserted_records::', inserted_records)
        return True

    @staticmethod
    def store_training_messages(db, sub_cat_id, my_info, assistant_info):
        request_message = my_info['message']
        word_confidences = my_info.get('word_confidences', [])

        response_message = assistant_info['message']

        user_id = 1
        cat_id = SubCategoryRepo().get(db, sub_cat_id).category_id
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        created_at = now
        updated_at = now

        # Insert user's message with word confidences
        user_message_query = """
        INSERT INTO social_media_conversation_messages (user_id, category_id, sub_category_id, role, content, audio_uri, mode, created_at, updated_at)
        VALUES (%s, %s, %s, 'user', %s, %s, %s, %s, %s)
        """
        execute_insert(user_message_query, (user_id, cat_id, sub_cat_id,
                       request_message, my_info['audio_uri'], 'training', created_at, updated_at))

        # Insert assistant's response
        assistant_message_query = """
        INSERT INTO social_media_conversation_messages (user_id, category_id, sub_category_id, role, content, audio_uri, mode, created_at, updated_at)
        VALUES (%s, %s, %s, 'assistant', %s, %s, %s, %s, %s)
        """
        execute_insert(assistant_message_query, (user_id, cat_id, sub_cat_id, response_message,
                       assistant_info['audio_uri'], 'training', created_at, updated_at))

        # Fetch inserted records to get message_id
        results = ConversationRepo.fetch_inserted_records(
            sub_cat_id, user_id, cat_id, created_at)
        message_id = results[0]['id'] if results else None

        # Save word confidences if message_id is valid
        if message_id:
            ConversationRepo.save_word_confidences(
                message_id, word_confidences)

        return {
            'records': results,
            'metadata': {}
        }

    @staticmethod
    async def store_interview_messages(db, request, sub_cat_id, my_info, assistant_info, interview_id):
        interview_question = await SharedRepo.get_interview_question(
            db, request, sub_cat_id, user_id=1)
        current_interview_message = SharedRepo.get_current_interview_message(
            interview_id, role='user')

        interview_question['is_completed'] = interview_question['is_completed'] and interview_question[
            'last_question_id'] == current_interview_message['question_id']

        if interview_question['is_completed']:
            return {
                'records': [],
                'metadata': {
                    'question_number': interview_question['question_number'],
                    'is_completed': True
                }
            }

        request_message = my_info['message']
        word_confidences = my_info.get('word_confidences', [])

        response_message = assistant_info['message']

        user_id = 1
        cat_id = SubCategoryRepo().get(db, sub_cat_id).category_id
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        created_at = now
        updated_at = now

        # Insert user's message with word confidences
        message = SharedRepo.get_current_interview_message(
            interview_id, role='assistant')
        prev_question_id = message['question_id'] if message else None

        user_message_query = """
        INSERT INTO social_media_conversation_messages (user_id, category_id, sub_category_id, role, mode, content, audio_uri, interview_id, question_id, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        execute_insert(user_message_query, (user_id, cat_id, sub_cat_id, 'user', 'interview',
                       request_message, my_info['audio_uri'], interview_id, prev_question_id, created_at, updated_at))

        # Insert assistant's response
        session = SharedRepo.get_session_by_id(interview_id)
        interview_id = session['id'] if session else None
        question_id = session['current_question_id'] if session else None

        assistant_message_query = """
        INSERT INTO social_media_conversation_messages (user_id, category_id, sub_category_id, role, mode, content, audio_uri, interview_id, question_id, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        execute_insert(assistant_message_query, (user_id, cat_id, sub_cat_id, 'assistant', 'interview',
                       response_message, assistant_info['audio_uri'], interview_id, question_id, created_at, updated_at))

        interview_question = await SharedRepo.get_interview_question(
            db, request, sub_cat_id, user_id=1)
        current_interview_message = SharedRepo.get_current_interview_message(
            interview_id, role='user')
        interview_question['is_completed'] = interview_question['is_completed'] and interview_question[
            'last_question_id'] == current_interview_message['question_id']

        results = ConversationRepo.fetch_inserted_records(
            sub_cat_id, user_id, cat_id, created_at)
        message_id = results[0]['id'] if results else None

        # Save word confidences if message_id is valid
        if message_id:
            ConversationRepo.save_word_confidences(
                message_id, word_confidences)

        return {
            'records': results,
            'metadata': {
                'question_number': interview_question['question_number'],
                'is_completed': interview_question['is_completed']
            }
        }

    @staticmethod
    async def store_messages(db, request, sub_cat_id, my_info, assistant_info, mode='training', interview_id=None):
        if mode == 'training':
            resp = ConversationRepo.store_training_messages(db,
                                                            sub_cat_id, my_info, assistant_info)
        else:
            resp = await ConversationRepo.store_interview_messages(db, request,
                                                             sub_cat_id, my_info, assistant_info, interview_id)

        # Return the inserted records
        return resp

    @staticmethod
    def fetch_inserted_records(sub_cat_id, user_id, cat_id, created_at):
        query = """
        SELECT * FROM social_media_conversation_messages
        WHERE user_id = %s AND category_id = %s AND sub_category_id = %s AND created_at = %s
        """
        return execute_query(query, (user_id, cat_id, sub_cat_id, created_at))

    @staticmethod
    def archive_messages(cat_id: int, sub_cat_id: int = None, mode='training'):
        if sub_cat_id:
            query = "UPDATE social_media_conversation_messages SET status_id = 0 WHERE sub_category_id = %s AND mode = %s"
            execute_query(query, (sub_cat_id, mode))
        else:
            query = "UPDATE social_media_conversation_messages SET status_id = 0 WHERE category_id = %s AND mode = %s"
            execute_query(query, (cat_id, mode))
        if mode == 'interview':
            query = "UPDATE conversation_v2_interviews SET status_id = 0 WHERE sub_category_id = %s"
            execute_query(query, (sub_cat_id,))

    @staticmethod
    def reset_messages(cat_id, sub_cat_id=None):
        if sub_cat_id:
            query = "DELETE FROM social_media_conversation_messages WHERE sub_category_id = %s"
            execute_query(query, (sub_cat_id,))
        else:
            query = "DELETE FROM social_media_conversation_messages WHERE category_id = %s"
            execute_query(query, (cat_id,))

    @staticmethod
    def add_message(user_id, cat_id, sub_cat_id, role, content, audio_uri, mode='training'):
        query = "INSERT INTO social_media_conversation_messages (user_id, category_id, sub_category_id, role, content, audio_uri, mode) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (user_id, cat_id, sub_cat_id, role, content, audio_uri, mode)
        execute_insert(query, values)

    @staticmethod
    def get_training_instructions(sub_cat):
        learn_instructions = sub_cat.learn_instructions

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
    async def get_interview_instructions(db, request, sub_cat):
        cat_name = CategoryRepo().get(db, sub_cat.category_id).name
        learn_instructions = f'You are interviewing a user on "{cat_name} - {sub_cat.name}".'
 
        res = await SharedRepo.get_interview_question(
            db, request, sub_cat.id, user_id=1, update=True)
        print('res::: --->', res)

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
    async def get_recent_messages(db, request, sub_cat_id, mode='training'):
        sub_cat = SubCategoryRepo().get(db, sub_cat_id)
        if not sub_cat:
            raise ValueError(f"Invalid sub-category ID: {sub_cat_id}")

        interview_id = None
        if mode == 'training':
            learn_instructions = ConversationRepo.get_training_instructions(
                sub_cat)
        else:
            learn_instructions, interview_id = await ConversationRepo.get_interview_instructions(
                db, request, sub_cat)

        messages = [{'content': learn_instructions, 'role': 'system'}]

        query = """
        SELECT content, role FROM social_media_conversation_messages 
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

    @staticmethod
    def save_word_confidences(message_id, word_confidences):

        if not word_confidences:
            return

        query = """
        INSERT INTO soccc_media_conversation_messages_word_confidences (message_id, word, confidence, start_time_seconds, end_time_seconds)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = [(message_id, wc['word'], wc['confidence'], wc['start_time'], wc['end_time'])
                  for wc in word_confidences]

        print(values)

        try:
            for value in values:
                execute_insert(query, value)
        except IntegrityError as e:
            print(f"IntegrityError: {e}")
