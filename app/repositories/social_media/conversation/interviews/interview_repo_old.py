# app/repositories/interviews.py
from app.database.old_connection import execute_query
from app.repositories.social_media.conversation.shared import SharedRepo
from app.repositories.social_media.conversation.categories.sub_categories.questions.question_repo import QuestionRepo
from app.services.social_media.conversation.openai_services import OpenAIService
from collections import defaultdict

class InterviewRepo:

    @staticmethod
    def get_interview_session(sub_cat_id, user_id):
        query_session = "SELECT id, current_question_id FROM social_media_conversation_interviews WHERE user_id = %s AND sub_category_id = %s AND status_id = %s"
        session = execute_query(
            query_session, (user_id, sub_cat_id, 1), fetch_method='first')
        return session

    @staticmethod
    async def get_interview_progress(db,request, sub_cat_id):
        # Merge the sub_category_id into the request's state params
        request.state.sub_category_id = str(sub_cat_id)
        request.state.order_by = 'id'
        request.state.order_direction = 'desc'

        interview = InterviewRepo.get_interview_session(sub_cat_id, 1)
        interview_id = interview['id'] if interview else None
        
        # Step 1: Query the database to get the list of questions
        questions = (await QuestionRepo().list(db, request))['records']

        # Step 2: Retrieve the session messages using sub_cat_id and the interview_id
        response = await SharedRepo.get_sub_cat_conversation(db, request,
            sub_cat_id, 'interview', interview_id)
        messages = response['records']

        current_question_id = None
        if len(messages):
            messages = [
                message for message in messages if message['role'] == 'user']
            current_question_id = messages[-1]['question_id']

        current_question = 0
        if current_question_id:
            # Step 3: Determine the current question's index
            current_question = next((index for index, item in enumerate(
                questions) if item.id == current_question_id), 0) + 1

        # Step 4: Construct and return the response
        response = {
            'interview_id': interview_id,
            'current_question': current_question,
            'total_count': len(questions) if questions else 0
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
        query_update_session = "select status_id from social_media_conversation_interviews WHERE id = %s"
        interview = execute_query(
            query_update_session, (interview_id,), fetch_method='first')

        if not interview['status_id'] == 2:
            return None

        query = """
        SELECT question_id, question_scores as score, content AS answer, soc4bversation_categories_sub_categories_questions.question, soc4bversation_categories_sub_categories_questions.marks as max_score 
        FROM social_media_conversation_messages
        JOIN soc4bversation_categories_sub_categories_questions on social_media_conversation_messages.question_id = soc4bversation_categories_sub_categories_questions.id
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
            "records": results,
            "total_score": total_score,
            "max_score": max_score,
            "percentage_score": percentage_score
        }

    @staticmethod
    def new_results_assessment(interview_id):
        query = "SELECT id, role, question_id, content FROM social_media_conversation_messages WHERE interview_id = %s"
        messages = execute_query(query, (interview_id,))

        # Fetch the actual questions and marks
        for msg in messages:
            if msg['role'] == 'user' and msg['question_id']:
                question_query = "SELECT question, marks FROM soc4bversation_categories_sub_categories_questions WHERE id = %s"
                question_result = execute_query(
                    question_query, (msg['question_id'],), fetch_method='first')
                if question_result:
                    msg['question'] = question_result['question']
                    msg['marks'] = question_result['marks']

        scores = OpenAIService().fetch_openai_interview_scores(messages)

        if scores and len(scores) > 0:
            InterviewRepo.update_interview_scores(interview_id, scores)

        # Calculate total and maximum score
        total_score = sum(int(score['score'])
                          for score in scores if score['score'] is not None)
        max_score = sum(int(score['max_score']) for score in scores)
        percentage_score = (total_score / max_score) * \
            100 if max_score > 0 else 0
        percentage_score = round(percentage_score)

        # notify_new_interview_results(interview_id)

        return {
            "records": scores,
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
            insert_query = "UPDATE social_media_conversation_messages SET question_scores = %s where id = %s"
            execute_query(insert_query, (score['score'], score['id']))

        percentage_score = round(
            total_scores / max_scores * 100) if total_scores else 0

        query_update_session = "UPDATE social_media_conversation_interviews SET status_id = 2, scores = %s, max_scores = %s, percentage_score = %s WHERE id = %s"
        execute_query(query_update_session, (total_scores,
                      max_scores, percentage_score, interview_id))

    # Add the listing methods below here
    @staticmethod
    def list_all_interviews():
        query = "SELECT * FROM social_media_conversation_interviews WHERE status_id = %s"
        results = execute_query(query, (2,))

        metadata = {
            'title': f'All interviews listing',
            'total_count': len(results) if results else 0,
        }

        response = {
            'records': results,
            'metadata': metadata
        }

        return response

    @staticmethod
    def list_interviews_by_category_id(category_id):
        query = "SELECT * FROM social_media_conversation_interviews WHERE category_id = %s AND status_id = %s"
        results = execute_query(query, (category_id, 2))

        metadata = {
            'title': f'Interviews listing for Category ID: {category_id}',
            'total_count': len(results) if results else 0
        }

        response = {
            'records': results,
            'metadata': metadata
        }

        return response

    @staticmethod
    def list_interviews_by_category_sub_category_id(category_id, sub_category_id, status_id=None):
        base_query = """
        SELECT social_media_conversation_interviews.*, soc7e_media_conversation_categories_sub_categories.name AS sub_category_name, soc4bversation_categories_sub_categories_questions.question AS question, soc4bversation_categories_sub_categories_questions.marks AS max_score, social_media_conversation_messages.question_scores AS score
        FROM social_media_conversation_interviews
        JOIN soc7e_media_conversation_categories_sub_categories ON social_media_conversation_interviews.sub_category_id = soc7e_media_conversation_categories_sub_categories.id
        LEFT JOIN social_media_conversation_messages ON social_media_conversation_interviews.id = social_media_conversation_messages.interview_id AND social_media_conversation_messages.role = 'user'
        LEFT JOIN soc4bversation_categories_sub_categories_questions ON social_media_conversation_messages.question_id = soc4bversation_categories_sub_categories_questions.id
        WHERE social_media_conversation_interviews.category_id = %s AND social_media_conversation_interviews.sub_category_id = %s
        """
        params = [category_id, sub_category_id]

        if status_id is not None and status_id != 0:
            base_query += " AND social_media_conversation_interviews.status_id = %s"
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
            'records': results,
            'metadata': metadata
        }

        return response

    @staticmethod
    def list_completed_interviews_grouped_by_category():
        query = """
        SELECT social_media_conversation_interviews.*, social_media_conversation_categories.name AS category_name, soc7e_media_conversation_categories_sub_categories.name AS subcategory_name, soc7e_media_conversation_categories_sub_categories.id AS subcategory_id
        FROM social_media_conversation_interviews
        JOIN social_media_conversation_categories ON social_media_conversation_interviews.category_id = social_media_conversation_categories.id
        LEFT JOIN soc7e_media_conversation_categories_sub_categories ON social_media_conversation_interviews.sub_category_id = soc7e_media_conversation_categories_sub_categories.id
        WHERE social_media_conversation_interviews.status_id = %s
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
            'records': grouped_results,
            'metadata': metadata
        }

    @staticmethod
    def list_completed_interviews_grouped_by_sub_categories(cat_id):
        query = """
        SELECT social_media_conversation_interviews.*, soc7e_media_conversation_categories_sub_categories.id AS sub_category_id, soc7e_media_conversation_categories_sub_categories.name AS sub_category_name
        FROM social_media_conversation_interviews
        JOIN soc7e_media_conversation_categories_sub_categories ON social_media_conversation_interviews.sub_category_id = soc7e_media_conversation_categories_sub_categories.id
        WHERE social_media_conversation_interviews.status_id = %s AND social_media_conversation_interviews.category_id = %s
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
            'records': grouped_results,
            'metadata': metadata
        }
