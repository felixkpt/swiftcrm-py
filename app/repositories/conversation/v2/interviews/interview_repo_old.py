# app/repositories/interviews.py
from app.database.old_connection import execute_query
from app.repositories.conversation.v2.shared import SharedRepo
from app.services.conversation.v2.openai_requests import fetch_openai_interview_scores
from collections import defaultdict


class InterviewRepo:

    @staticmethod
    def get_interview_session(sub_cat_id, user_id):
        query_session = "SELECT id, current_question_id FROM conversation_v2_interviews WHERE user_id = %s AND sub_category_id = %s AND status_id = %s"
        session = execute_query(
            query_session, (user_id, sub_cat_id, 1), fetch_method='first')
        return session

    @staticmethod
    def get_interview_progress(db, sub_cat_id, interview_id):
        # Step 1: Query the database to get the list of questions
        query = "SELECT * FROM conversation_v2_categories_sub_categories_questions WHERE sub_category_id = %s"
        results = execute_query(query, (sub_cat_id,))

        # Step 2: Retrieve the session messages using sub_cat_id and the interview_id
        response = SharedRepo.get_sub_cat_conversation(db, 
            sub_cat_id, 'interview', interview_id)
        messages = response['results']

        current_question_id = None
        if len(messages):
            messages = [
                message for message in messages if message['role'] == 'user']
            current_question_id = messages[-1]['question_id']

        current_question = 0
        if current_question_id:
            # Step 3: Determine the current question's index
            print('current_question_id:', current_question_id)
            current_question = next((index for index, item in enumerate(
                results) if item['id'] == current_question_id), 0) + 1

        # Step 4: Construct and return the response
        response = {
            'current_question': current_question,
            'total_count': len(results) if results else 0
        }

        return response

    @staticmethod
    def get_interview_results(interview_id):
        results = InterviewRepo.get_existing_results(interview_id)

        if not results:
            results = InterviewRepo.new_results_assessment(interview_id)
        return results

    @staticmethod
    def get_existing_results(interview_id):
        query_update_session = "select status_id from conversation_v2_interviews WHERE id = %s"
        interview = execute_query(
            query_update_session, (interview_id,), fetch_method='first')

        if not interview['status_id'] == 2:
            return None

        query = """
        SELECT question_id, question_scores as score, content AS answer, conversation_v2_categories_sub_categories_questions.question, conversation_v2_categories_sub_categories_questions.marks as max_score 
        FROM conversation_v2_messages
        JOIN conversation_v2_categories_sub_categories_questions on conversation_v2_messages.question_id = conversation_v2_categories_sub_categories_questions.id
        WHERE interview_id = %s AND role = 'user' AND question_id IS NOT NULL
        """

        results = execute_query(query, (interview_id,))

        total_score = sum(int(score['score'])
                          for score in results if score['score'] is not None)
        max_score = sum(int(score['max_score']) for score in results)
        percentage_score = (total_score / max_score) * \
            100 if max_score > 0 else 0
        percentage_score = round(percentage_score)

        return {
            "results": results,
            "total_score": total_score,
            "max_score": max_score,
            "percentage_score": percentage_score
        }

    @staticmethod
    def new_results_assessment(interview_id):
        query = "SELECT id, role, question_id, content FROM conversation_v2_messages WHERE interview_id = %s"
        messages = execute_query(query, (interview_id,))

        # Fetch the actual questions and marks
        for msg in messages:
            if msg['role'] == 'user' and msg['question_id']:
                question_query = "SELECT question, marks FROM conversation_v2_categories_sub_categories_questions WHERE id = %s"
                question_result = execute_query(
                    question_query, (msg['question_id'],), fetch_method='first')
                if question_result:
                    msg['question'] = question_result['question']
                    msg['marks'] = question_result['marks']

        scores = fetch_openai_interview_scores(messages)

        if scores and len(scores) > 0:
            InterviewRepo.update_interview_scores(interview_id, scores)

        # Calculate total and maximum score
        total_score = sum(int(score['score'])
                          for score in scores if score['score'] is not None)
        max_score = sum(int(score['max_score']) for score in scores)
        percentage_score = (total_score / max_score) * \
            100 if max_score > 0 else 0
        percentage_score = round(percentage_score)

        return {
            "results": scores,
            "total_score": total_score,
            "max_score": max_score,
            "percentage_score": percentage_score
        }

    @staticmethod
    def update_interview_scores(interview_id, scores):
        # Insert new scores
        total_scores = 0
        max_scores = 0
        for score in scores:
            total_scores += score['score']
            max_scores += score['max_score']
            insert_query = "UPDATE conversation_v2_messages SET question_scores = %s where id = %s"
            execute_query(insert_query, (score['score'], score['id']))

        percentage_score = round(
            total_scores / max_scores * 100) if total_scores else 0

        query_update_session = "UPDATE conversation_v2_interviews SET status_id = 2, scores = %s, max_scores = %s, percentage_score = %s WHERE id = %s"
        execute_query(query_update_session, (total_scores,
                      max_scores, percentage_score, interview_id))

    # Add the listing methods below here
    @staticmethod
    def list_all_interviews():
        query = "SELECT * FROM conversation_v2_interviews WHERE status_id = %s"
        results = execute_query(query, (2,))

        metadata = {
            'title': f'All interviews listing',
            'total_count': len(results) if results else 0,
        }

        response = {
            'results': results,
            'metadata': metadata
        }

        return response

    @staticmethod
    def list_interviews_by_category_id(category_id):
        query = "SELECT * FROM conversation_v2_interviews WHERE category_id = %s AND status_id = %s"
        results = execute_query(query, (category_id, 2))

        metadata = {
            'title': f'Interviews listing for Category ID: {category_id}',
            'total_count': len(results) if results else 0
        }

        response = {
            'results': results,
            'metadata': metadata
        }

        return response

    @staticmethod
    def list_interviews_by_category_sub_category_id(category_id, sub_category_id, status_id=None):
        base_query = """
        SELECT conversation_v2_interviews.*, conversation_v2_categories_sub_categories.name AS sub_category_name, conversation_v2_categories_sub_categories_questions.question AS question, conversation_v2_categories_sub_categories_questions.marks AS max_score, conversation_v2_messages.question_scores AS score
        FROM conversation_v2_interviews
        JOIN conversation_v2_categories_sub_categories ON conversation_v2_interviews.sub_category_id = conversation_v2_categories_sub_categories.id
        LEFT JOIN conversation_v2_messages ON conversation_v2_interviews.id = conversation_v2_messages.interview_id AND conversation_v2_messages.role = 'user'
        LEFT JOIN conversation_v2_categories_sub_categories_questions ON conversation_v2_messages.question_id = conversation_v2_categories_sub_categories_questions.id
        WHERE conversation_v2_interviews.category_id = %s AND conversation_v2_interviews.sub_category_id = %s
        """
        params = [category_id, sub_category_id]

        if status_id is not None and status_id != 0:
            base_query += " AND conversation_v2_interviews.status_id = %s"
            params.append(status_id)

        results = execute_query(base_query, tuple(params)) or []

        # Calculate scores
        for result in results:
            result['score'] = result['score'] if result['score'] is not None else 0

        metadata = {
            'title': f'Interviews listing for Category ID: {category_id}, sub_category ID: {sub_category_id}',
            'total_count': len(results) if results else 0
        }

        response = {
            'results': results,
            'metadata': metadata
        }

        return response

    @staticmethod
    def list_completed_interviews_grouped_by_category():
        query = """
        SELECT conversation_v2_interviews.*, conversation_v2_categories.name AS category_name, conversation_v2_categories_sub_categories.name AS subcategory_name, conversation_v2_categories_sub_categories.id AS subcategory_id
        FROM conversation_v2_interviews
        JOIN conversation_v2_categories ON conversation_v2_interviews.category_id = conversation_v2_categories.id
        LEFT JOIN conversation_v2_categories_sub_categories ON conversation_v2_interviews.sub_category_id = conversation_v2_categories_sub_categories.id
        WHERE conversation_v2_interviews.status_id = %s
        """
        results = execute_query(query, (2,))

        # Group interviews by category and subcategory
        categories_map = defaultdict(lambda: defaultdict(list))
        for result in results:
            category_id = result['category_id']
            subcategory_id = result['subcategory_id']
            categories_map[category_id][subcategory_id].append(result)

        # Prepare response
        grouped_results = []
        for category_id, sub_categories in categories_map.items():
            category_name = None
            subcategory_results = []
            subcategory_count = 0
            for subcategory_id, interviews in sub_categories.items():
                if not category_name:
                    category_name = interviews[0]['category_name']
                subcategory_name = interviews[0]['subcategory_name'] if interviews[0]['subcategory_name'] else "Uncategorized"
                total_count = len(interviews)
                subcategory_results.append({
                    'id': subcategory_id,
                    'name': subcategory_name,
                    'interviews': interviews,
                    'total_count': total_count
                })
                subcategory_count += total_count

            grouped_results.append({
                'id': category_id,
                'name': category_name,
                'sub_categories': subcategory_results,
                'total_count': subcategory_count
            })

        metadata = {
            'title': f'Listing ({len(results)}) Interviews done in Categories',
            # Total count of all categories
            'total_count': len(grouped_results)
        }

        return {
            'results': grouped_results,
            'metadata': metadata
        }

    @staticmethod
    def list_completed_interviews_grouped_by_sub_categories(cat_id):
        query = """
        SELECT conversation_v2_interviews.*, conversation_v2_categories_sub_categories.id AS sub_category_id, conversation_v2_categories_sub_categories.name AS sub_category_name
        FROM conversation_v2_interviews
        JOIN conversation_v2_categories_sub_categories ON conversation_v2_interviews.sub_category_id = conversation_v2_categories_sub_categories.id
        WHERE conversation_v2_interviews.status_id = %s AND conversation_v2_interviews.category_id = %s
        """
        results = execute_query(query, (2, cat_id))

        # Group interviews by sub_category
        sub_categories_map = defaultdict(list)
        for result in results:
            sub_category_id = result['sub_category_id']
            sub_category_name = result['sub_category_name']
            sub_categories_map[(sub_category_id, sub_category_name)].append(
                result)

        # Prepare response
        grouped_results = []
        for (sub_category_id, sub_category_name), interviews in sub_categories_map.items():
            total_count = len(interviews)

            grouped_results.append({
                'id': sub_category_id,
                'name': sub_category_name,
                'interviews': interviews,
                'total_count': total_count
            })

        metadata = {
            'title': f'Listing ({len(results)}) Interviews done in Category {cat_id}',
            'total_count': len(results)  # Total count of all interviews
        }

        return {
            'results': grouped_results,
            'metadata': metadata
        }
