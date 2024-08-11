# app/services/social_media/conversation/openai_requests.py
import openai
from decouple import Config, RepositoryEnv
import re

DOTENV_FILE = '.env'
env_config = Config(RepositoryEnv(DOTENV_FILE))

OPEN_AI_ORG = env_config.get('OPEN_AI_ORG')
OPEN_AI_KEY = env_config.get('OPEN_AI_KEY')

print('OPEN_AI_ORG:', OPEN_AI_ORG)

# Retrieve Env vars
openai.organization = OPEN_AI_ORG
openai.api_key = OPEN_AI_KEY

# Open AI - Whisper
# Convert Audio to Text


def convert_audio_to_text(audio_file):

    try:
        transcript = openai.Audio.transcribe('whisper-1', audio_file)
        print('transcript', transcript)
        message_text = transcript['text']
        return message_text
    except Exception as e:
        print(e)
        return

# Open AI - ChatGPT
# Get response to our Messages


def get_chat_message_response(messages, interview_id, message_content, sub_cat_id, mode):
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
        return


def fetch_openai_interview_scores(messages):
    scores = []

    for msg in messages:
        if msg['role'] == 'user' and 'question' in msg:
            instructions = f'Assign marks to the question: "{msg["question"]}". PLEASE assign INTERGER ONLY BASED ON THE USER ANSWER: 0 - {msg["marks"]} marks, DONT COMMENT'
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
                # print(f'Score for question {msg["question_id"]}:', score)
            except Exception as e:
                print(e)
                scores.append(
                    {'question_id': msg['question_id'], 'score': None})

    return scores


def analyze_transcript(transcript):
    words = transcript.split()
    results = []

    for word in words:
        fluency, accuracy = analyze_word(word)
        results.append({
            'word': word,
            'fluency': fluency,
            'accuracy': accuracy
        })

    return results


def analyze_word(word):
    instructions = (
        f"Assess the fluency and accuracy of the word: '{word}'. "
        "Provide scores in the format: 'Fluency: <score> Accuracy: <score>'. "
        "Use a range from 0 to 10 where 0 means poor and 10 means excellent."
    )

    formatted_messages = [
        {'role': 'system', 'content': instructions},
        {'role': 'user', 'content': word}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=formatted_messages
        )
        result = response['choices'][0]['message']['content']

        # Regex to extract fluency and accuracy scores
        fluency_match = re.search(r'Fluency:\s*(\d+)', result)
        accuracy_match = re.search(r'Accuracy:\s*(\d+)', result)

        fluency = int(fluency_match.group(1)) if fluency_match else None
        accuracy = int(accuracy_match.group(1)) if accuracy_match else None

        return fluency, accuracy
    except Exception as e:
        print(e)
        return None, None


def calculate_averages(word_results):
    total_fluency = 0
    total_accuracy = 0
    count = 0

    for result in word_results:
        if result['fluency'] is not None:
            total_fluency += result['fluency']
            total_accuracy += result['accuracy']
            count += 1

    average_fluency = total_fluency / count if count > 0 else 0
    average_accuracy = total_accuracy / count if count > 0 else 0

    return average_fluency, average_accuracy
