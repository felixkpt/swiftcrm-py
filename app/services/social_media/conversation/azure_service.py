import azure.cognitiveservices.speech as speechsdk
from decouple import Config, RepositoryEnv

class AzureService:
    def __init__(self):
        # Load environment variables

        self.env_config = Config(RepositoryEnv('.env'))
        self.speech_key = self.env_config.get('AZURE_SPEECH_KEY')
        self.region = self.env_config.get('AZURE_REGION')
        print('AZURE_REGION:', self.region)

        self.speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.region)

    def upload_to_azure(self, source_file, destination_file):
        # Implement your Azure Blob Storage upload logic here
        pass

    def transcribe_speech(self, audio_file_path):
        audio_config = speechsdk.AudioConfig(filename=audio_file_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)

        result = speech_recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return {"transcript_text": result.text, "word_confidences": []}
        elif result.reason == speechsdk.ResultReason.NoMatch:
            raise HTTPException(status_code=400, detail="No speech could be recognized")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            raise HTTPException(status_code=400, detail=f"Speech Recognition canceled: {cancellation_details.reason}")

    def convert_text_to_speech(self, text, file_path):
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config)
        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            with open(file_path, 'wb') as audio_file:
                audio_file.write(result.audio_data)
            return file_path
        else:
            raise HTTPException(status_code=400, detail="Failed to convert text to speech")
