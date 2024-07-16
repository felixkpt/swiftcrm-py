from datetime import datetime
from app.database.old_connection import execute_query
from app.repositories.conversation.v2.categories.sub_categories.sub_category_repo import SubCategoryRepo
from app.repositories.conversation.v2.categories.sub_categories.questions.question_repo import QuestionRepo
from app.database.old_connection import execute_query, execute_insert


class SharedRepo:

    @staticmethod
    def get_session_by_id(interview_id):
        query_session = "SELECT * FROM conversation_v2_interviews WHERE id = %s AND status_id = %s"
        session = execute_query(
            query_session, (interview_id, 1), fetch_method='first')
        return session

    @staticmethod
    def get_interview_question(db, sub_cat_id, user_id, update=False):
        cat_id = SubCategoryRepo.get(db, sub_cat_id).id

        questions = QuestionRepo.get_sub_cat_questions(db, sub_cat_id)[
            'results']

        query_session = "SELECT id, current_question_id FROM conversation_v2_interviews WHERE user_id = %s AND category_id = %s AND sub_category_id = %s AND status_id = %s"
        session = execute_query(
            query_session, (user_id, cat_id, sub_cat_id, 1), fetch_method='first')

        question_number = 0
        last_question_id = questions[-1].id
        is_completed = False

        if not session:
            if update:
                question_number = 1
                # Create a new session if none exists
                question_id = questions[0].id
                query_insert_session = """
                INSERT INTO conversation_v2_interviews (user_id, category_id, sub_category_id, current_question_id, created_at, updated_at)
                VALUES (%s, %s, %s,%s, %s, %s)
                """
                interview_id = execute_insert(
                    query_insert_session, (user_id, cat_id, sub_cat_id, question_id, datetime.now(), datetime.now()))
                session = {'id': interview_id,
                           'current_question_id': question_id}

        else:
            # Find the current question index and move to the next question
            current_question_id = session['current_question_id']
            question_ids = [q.id for q in questions]
            try:
                current_index = question_ids.index(current_question_id)
                question_number = current_index + 1
                next_question_id = question_ids[current_index + 1]
                question_number += 1
            except (ValueError, IndexError):
                # Handle case where current question is not found or there is no next question
                next_question_id = None
                is_completed = True

            if next_question_id and update:
                query_update_session = """
                UPDATE conversation_v2_interviews SET current_question_id = %s, updated_at = %s WHERE id = %s
                """
                execute_query(query_update_session,
                              (next_question_id, datetime.now(), session['id']))
                session['current_question_id'] = next_question_id

        question = QuestionRepo.get(db, session['current_question_id'])        
        question = question.question

        interview_id = session['id']
        return {
            'question': question,
            'question_number': question_number,
            'last_question_id': last_question_id,
            'is_completed': is_completed,
            'interview_id': interview_id,
        }

    @staticmethod
    def get_current_interview_message(interview_id, role='assistant'):

        # Construct the query to fetch the corresponding message from the database
        query_fetch_message = """
        SELECT * FROM conversation_v2_messages
        WHERE interview_id = %s
        AND role = %s
        AND status_id = %s
        ORDER BY created_at DESC
        LIMIT 1
        """
        message_record = execute_query(
            query_fetch_message, (interview_id, role, 1), fetch_method='first')

        return message_record

    @staticmethod
    def get_sub_cat_conversation(db, sub_cat_id, mode='training', interview_id=None):
        if mode not in ['training', 'interview']:
            raise ValueError("Mode must be either 'training' or 'interview'")

        if interview_id and int(interview_id) > 0:
            query = """
            SELECT * FROM conversation_v2_messages 
            WHERE sub_category_id = %s 
            AND mode = %s 
            AND interview_id = %s 
            AND status_id = %s
            ORDER BY id ASC
            """
            params = (sub_cat_id, mode, interview_id, 1)
        else:
            query = """
            SELECT * FROM conversation_v2_messages 
            WHERE sub_category_id = %s 
            AND mode = %s 
            AND interview_id IS NULL 
            AND status_id = %s
            ORDER BY id ASC
            """
            params = (sub_cat_id, mode, 1)

        results = execute_query(query, params)

        metadata = {
            'title': 'Conversation list',
            'total_count': len(results) if results else 0,
        }

        if mode == 'interview':
            progress = SharedRepo.interview_progress(db, interview_id, sub_cat_id)
            metadata['question_number'] = progress['question_number']
            metadata['is_completed'] = progress['is_completed']

        response = {
            'results': results,
            'metadata': metadata
        }

        return response

    @staticmethod
    def interview_progress(db, interview_id, sub_cat_id):
        interview_question = SharedRepo.get_interview_question(db, 
            sub_cat_id, user_id=1)
        current_interview_message = SharedRepo.get_current_interview_message(
            interview_id, role='user')

        interview_question['is_completed'] = interview_question['is_completed'] and current_interview_message is not None and interview_question[
            'last_question_id'] == current_interview_message['question_id']

        return interview_question
