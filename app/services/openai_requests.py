from app.models.conversation import get_recent_messages
import openai
from decouple import config

# Retrieve Env vars
openai.organization = config('OPEN_AI_ORG')
openai.api_key = config('OPEN_AI_KEY')
openai.ln = 'en'

# Open AI - Whisper
# Convert Audio to Text


def convert_audio_to_text(audio_file):
    try:
        transcript = openai.Audio.transcribe('whisper-1', audio_file)
        message_text = transcript['text']
        return message_text
    except Exception as e:
        print(e)
        return

# Open AI - ChatGPT
# Get response to our Messages


def get_chat_response(message_content, sub_cat_id):
    messages = get_recent_messages(sub_cat_id)
    user_message = {'role': 'user', 'content': message_content}
    messages.append(user_message)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        message_text = response['choices'][0]['message']['content']
        return message_text

    except Exception as e:
        print(e)
        return
