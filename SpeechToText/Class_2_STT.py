from google.cloud import speech_v1
import soundfile
import sounddevice
import io
from scipy.io.wavfile import write

j_path = r'X:\Python Files\vision-project-207707-a6f8a24427c5.json'
client = speech_v1.SpeechClient.from_service_account_json(j_path)


def stt(myTime):
    sampleRate = 44100
    recDurationSeconds = myTime
    totalNumSamples = int(sampleRate*recDurationSeconds)

    print("Started Recordning")
    myRecording = sounddevice.rec(totalNumSamples,sampleRate,1)
    sounddevice.wait()
    print("recording Finished")

    write("voiceRecordning.wav", sampleRate, myRecording)
    data, recordingSampleRate = soundfile.read("voiceRecordning.wav")
    soundfile.write("VoiceRecording.flac", data, sampleRate)

    encoding = speech_v1.RecognitionConfig.AudioEncoding.FLAC
    langCode = 'en-CA'
    config = {'encoding':encoding, 'sample_rate_hertz':sampleRate, 'language_code':langCode}

    myAduiFile = r"VoiceRecording.flac"
    with io.open(myAduiFile, 'rb') as audio_file:
        content = audio_file.read()
        audio = speech_v1.RecognitionAudio(content=content)
        response = client.recognize(config=config,audio=audio)

    try:
        return response.results[0].alternatives[0].transcript.lower()
    except:
        return None
