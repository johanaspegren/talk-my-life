import os
import openai
import config

from modules.Mouth_ios import Speech
from modules.Ear_ios import Ear
from modules.Brain import Memory

speech = Speech()
ear = Ear()
memory = Memory()

openai.api_key = config.OPENAI_API_KEY



initalGreet = "I am great. Ask me about my day."
conversationStarter = [
    {"role": "system", "content": "You are a close friend and great listener, you are very interested in my life."},
    {"role": "user", "content": "You will ask me questions and try and learn as much as possible about me and my family."},
    {"role": "assistant", "content": "Hi, how are you today!"},
    {"role": "user", "content": initalGreet}
]

def askOpenai(_conversation):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=_conversation
        )
    return response.choices[0].message.content

# user (implicit)
# assistant (tell me of your day)
print('start')
keepGoing = True
thisConversation = conversationStarter
while keepGoing:
    assistantResponse = askOpenai(thisConversation)
    print('chatty: %s', assistantResponse)
    speech.say(assistantResponse)
    thisConversation.append({"role": "assistant", "content": assistantResponse})
    memory.rememberThis({"role": "assistant", "content": assistantResponse})

    # prompt user 
    print ('please speak')
    userResponse = ear.listen()
    print('me: %s', userResponse)
    # keep going?
    if 'stop' in userResponse:
        keepGoing = False
    thisConversation.append({"role": "user", "content": userResponse})
    memory.rememberThis({"role": "user", "content": userResponse})


speech.say("Ok, see you later alligator. Loved the chat!")
