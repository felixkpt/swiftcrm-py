from google.cloud import texttospeech, speech, storage
from google.oauth2 import service_account
import os

# Load environment variables
GOOGLE_CLOUD_STORAGE_BUCKET = os.getenv('GOOGLE_CLOUD_STORAGE_BUCKET')
GCS_PROJECT_FOLDER = os.getenv('GCS_PROJECT_FOLDER')

# Define the path to the service account JSON file
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))))
credentials_path = os.path.join(
    BASE_DIR, '../gcs-storage-service-account.json')

# Load the credentials
credentials = service_account.Credentials.from_service_account_file(
    credentials_path)

# Initialize the Speech-to-Text client with the credentials
speech_client = speech.SpeechClient(credentials=credentials)


def convert_text_to_speech(text, destination_file_name):
    # Initialize the Text-to-Speech client
    client = texttospeech.TextToSpeechClient()

    # Set up the synthesis input with the provided text
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Configure the audio output format
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(destination_file_name, 'wb') as f:
        f.write(response.audio_content)
        file_path = f.name

    return file_path


def upload_to_gcs(source_file_name, destination_file_name):
    """Uploads a file to Google Cloud Storage and returns the public URI."""
    # Initialize a GCS client
    storage_client = storage.Client()
    bucket = storage_client.bucket(GOOGLE_CLOUD_STORAGE_BUCKET)

    # Define the blob path including the folder
    blob_path = f'{GCS_PROJECT_FOLDER}/{destination_file_name}'

    # Create a blob object
    blob = bucket.blob(blob_path)

    # Upload the file to the blob
    blob.upload_from_filename(source_file_name)

    # Make the blob publicly accessible
    blob.make_public()

    # Return the public URL
    return blob.public_url


def transcribe_speech(source_file_name):

    print('source_file_name',source_file_name)

    try:

        with open(source_file_name, "rb") as audio_file:
            audio_content = audio_file.read()

            audio = speech.RecognitionAudio(content=audio_content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
                sample_rate_hertz=48000,
                language_code="en-KE",
                model="default",
                audio_channel_count=1,
                enable_word_confidence=True,
                enable_word_time_offsets=True,
            )

            response = speech_client.recognize(config=config, audio=audio)

            transcript_text = ' '.join(
                [result.alternatives[0].transcript for result in response.results])

            word_confidences = []
            for result in response.results:
                for word in result.alternatives[0].words:
                    word_confidences.append({
                        "word": word.word,
                        "confidence": word.confidence,
                        "start_time": word.start_time.total_seconds(),
                        "end_time": word.end_time.total_seconds()
                    })

            return {
                'transcript_text': transcript_text,
                'word_confidences': word_confidences,
            }
        
    except Exception as e:
        print('transcribe_speech error:', e)
        return None
