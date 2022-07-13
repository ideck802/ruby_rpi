import requests
import pygame
import os
import time

#dirname = os.path.dirname(__file__)

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= dirname + "/../ruby-for-pc-0b5827d59846.json"
#voice = texttospeech.VoiceSelectionParams(
#    language_code='en-US',
#    name='en-US-Wavenet-H',
#    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
#google_tts_client = texttospeech.TextToSpeechClient()
pygame.mixer.init()

url = "https://eastus.tts.speech.microsoft.com/cognitiveservices/v1"
header = {
    'Ocp-Apim-Subscription-Key': " ",
    'Content-Type': 'application/ssml+xml',
    'X-Microsoft-OutputFormat': 'audio-24khz-160kbitrate-mono-mp3'
}

expression = "friendly"

def speak(phrase):
    data = """<speak xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xmlns:emo='http://www.w3.org/2009/10/emotionml' version='1.0' xml:lang='en-US'>\
<voice name='en-US-SaraNeural'>\
<mstts:express-as style='{}' ><prosody rate='10%' pitch='5%'>\
{}\
</prosody>\
</mstts:express-as>\
</voice>\
</speak>""".format(expression, phrase)
    
    try:
        response = requests.post(url, headers=header, data=data)
        response.raise_for_status()
        with open("./speech/speech_files/speak.mp3", "wb") as file:
            file.write(response.content)
        print(response)
        response.close()
        pygame.mixer.music.load("./speech/speech_files/speak.mp3")
        pygame.mixer.music.play()
        time.sleep(1)
    except Exception as e:
        print("ERROR: ", e)

#def speak(phrase):
#    response = google_tts_client.synthesize_speech(input=texttospeech.SynthesisInput(text=phrase), voice=voice, audio_config=texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3))
#    open(dirname + '/speech_files/speak.mp3', 'wb').write(response.audio_content)
#    pygame.mixer.music.load(dirname + "/speech_files/speak.mp3")
#    pygame.mixer.music.play()
#    time.sleep(1)
    
    
if __name__ == "__main__":
    speak("Hello!")