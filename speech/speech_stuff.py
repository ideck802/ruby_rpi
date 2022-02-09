from google.cloud import texttospeech
import pygame
import os
import time

dirname = os.path.dirname(__file__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= dirname + "/../ruby-for-pc-0b5827d59846.json"
voice = texttospeech.VoiceSelectionParams(
    language_code='en-US',
    name='en-US-Wavenet-H',
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
google_tts_client = texttospeech.TextToSpeechClient()
pygame.mixer.init()

def speak(phrase):
    response = google_tts_client.synthesize_speech(input=texttospeech.SynthesisInput(text=phrase), voice=voice, audio_config=texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3))
    open(dirname + '/speech_files/speak.mp3', 'wb').write(response.audio_content)
    pygame.mixer.music.load(dirname + "/speech_files/speak.mp3")
    pygame.mixer.music.play()
    time.sleep(1)
    
    
if __name__ == "__main__":
    speak("Hello!")