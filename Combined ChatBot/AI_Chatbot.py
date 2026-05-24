from google import genai
from Class_1_TTS import tts
from Class_2_STT import stt

API = "AIzaSyBeU8FwR7cvBPdjYSsHBAHTqlg107YhGnY"
client = genai.Client(api_key = API)
chat = client.chats.create(model="gemini-3-flash-preview")

while True:
        
    user = stt(4)
    response = chat.send_message(user + " Answer in 2 sentances")
    tts(response.text)
    print(response.text)


    for message in chat.get_history():
            print(f'role - {message.role}',end=": ")
            print(message.parts[0].text)
