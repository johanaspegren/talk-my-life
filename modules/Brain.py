# firebase
import json
import firebase_admin
from datetime import datetime
from firebase_admin import credentials, db

cred = credentials.Certificate("talk-of-my-life-firebase-adminsdk-1oeml-85cb0d118b.json")

class Memory:
    def __init__(self):
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://talk-of-my-life-default-rtdb.europe-west1.firebasedatabase.app/'
        })
        self.conversationsRef = db.reference('/conversations')

    def recall(self):
        rememberedConversations = self.conversationsRef.get()
        return rememberedConversations

    def rememberThis(self, _entry):
        dt = json.dumps(datetime.now(), default=str)
        self.conversationsRef.push({'msg':_entry, 'timestamp':dt})

