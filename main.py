import speech_recognition as sr

import config
import openai

import pyttsx3

# firebase
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("talk-of-my-life-firebase-adminsdk-1oeml-85cb0d118b.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://talk-of-my-life-default-rtdb.europe-west1.firebasedatabase.app/'
})

conversationsRef = db.reference('/conversations')

# push

conversationStarter = [
    {"role": "system", "content": "You are a close friend and great listener, you are very interested in my life."},
    {"role": "user", "content": "You will ask me questions and try and learn as much as possible about me and my family. Also, I will call you Chatty"},
    {"role": "assistant", "content": "Hi, how are you today!"}
]
# get the memories 
fetchedConversations = conversationsRef.get()
fetchedConversations = [] # temporarily clear memory
print (fetchedConversations)

thisConversation = []
# add them to this conversation
for key in fetchedConversations:
    thisConversation.append(
        {"role": fetchedConversations[key]['role'],
         "content": fetchedConversations[key]['content']}
    )
thisConversation.append(conversationStarter)


r = sr.Recognizer()
openai.api_key = config.OPENAI_API_KEY


def rememberThisPiece(_entry):
    conversationsRef.push(_entry)


def speakThis(_text):
    engine = pyttsx3.init()
    engine.say(_text)
    engine.runAndWait()


def captureSpeechInput():
    with sr.Microphone() as source:
        audio_data = r.listen(source)
        print("Recognizing...")
        text = r.recognize_google(audio_data)
        return(text)


def askOpenai(_conversation):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=_conversation
        )
    return response


speakThis("Hi, how are you today")

while True:
    spokenPrompt = ""
    try:
        spokenPrompt = captureSpeechInput()
    except:
        speakThis("sorry, didn´t catch that - try again")
        continue
        # startover

    print("spkprmpt: %s" %spokenPrompt)
    if(spokenPrompt.lower() == "stop"):
        keepGoing = False
        break
    
    #messages = generateMessagesFromPrompt(spokenPrompt)
    thisConversation.append({"role": "user", "content": spokenPrompt})
    rememberThisPiece({"role": "user", "content": spokenPrompt})
    print ("conversation :")
    print (thisConversation)
    answerString = ""

    try:
        answer = askOpenai(thisConversation)
        answerString = answer.choices[0].message.content
    except:
        answerString = "I experienced an error"

    print("answer:%s" %answerString)
    speakThis(answerString)
    thisConversation.append({"role": "assistant", "content": answerString})
    rememberThisPiece({"role": "assistant", "content": answerString})

#    speakThis("ok?")


speakThis("Cool, see you later alligator")


