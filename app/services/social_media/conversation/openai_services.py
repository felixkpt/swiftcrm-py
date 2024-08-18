import openai
from decouple import Config, RepositoryEnv
import re


class OpenAIService:
    def __init__(self, dotenv_file='.env'):
        self.env_config = Config(RepositoryEnv(dotenv_file))
        self.organization = self.env_config.get('OPEN_AI_ORG')
        self.api_key = self.env_config.get('OPEN_AI_KEY')

        openai.organization = self.organization
        openai.api_key = self.api_key

    # Open AI - Whisper
    # Convert Audio to Text
    def transcribe_speech(self, source_file_name):
        try:
            with open(source_file_name, "rb") as audio_file:

                transcript = openai.Audio.transcribe('whisper-1', audio_file)
                print('transcript', transcript)
                message_text = transcript['text']
                return message_text
        except Exception as e:
            print(f'OPEN AI transcribe_speech:{e}')
            return None

    # Open AI - ChatGPT
    # Get response to our Messages
    def get_chat_message_response(self, messages, interview_id, message_content, sub_cat_id, mode):
        user_message = {'role': 'user', 'content': message_content}
        messages.append(user_message)

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            message_text = response['choices'][0]['message']['content']
            return message_text, interview_id

        except Exception as e:
            print(e)
            return None, interview_id

    def fetch_openai_interview_scores(self, messages):
        scores = []

        for msg in messages:
            if msg['role'] == 'user' and 'question' in msg:
                instructions = f'Assign marks to the question: "{msg["question"]}". PLEASE assign INTEGER ONLY BASED ON THE USER ANSWER: 0 - {msg["marks"]} marks, DONT COMMENT'
                formatted_messages = [
                    {'role': 'system', 'content': instructions},
                    {'role': msg['role'], 'content': msg['content']}
                ]

                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=formatted_messages
                    )
                    score = int(response['choices'][0]['message']['content'])
                    scores.append({'id': msg['id'], 'question_id': msg['question_id'], 'max_score': msg['marks'],
                                   'question': msg['question'], 'answer': msg['content'], 'score': score})
                except Exception as e:
                    print(e)
                    scores.append(
                        {'question_id': msg['question_id'], 'score': None})

        return scores
