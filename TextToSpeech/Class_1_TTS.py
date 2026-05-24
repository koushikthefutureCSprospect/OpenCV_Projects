from google.cloud import texttospeech
import subprocess
import time

client = texttospeech.TextToSpeechClient.from_service_account_json(r'TTS_STT_creds.json')

languageCode = 'en-IN'
gender = texttospeech.SsmlVoiceGender.MALE

voice = texttospeech.VoiceSelectionParams(language_code = languageCode, ssml_gender = gender)
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

def tts(texts, delay=None):
    if delay == None:
        delay = len(texts) * 0.1
    

    synthesis_input = texttospeech.SynthesisInput(text = texts)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    with open("tts.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)

    mediaPlayerPath = r'c:\Program Files\Windows Media Player\wmplayer.exe'
    speak = r'z:\PY07\tts.mp3'

    play = subprocess.Popen([mediaPlayerPath,speak])
    time.sleep(delay)
    play.kill()