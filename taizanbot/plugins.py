# coding: utf-8

from slackbot.bot import respond_to, default_reply
from .models import Session, Speech
import random

@respond_to(ur'add (.+)')
def check(message, text):
    sess = Session()
    speech = Speech()
    speech.speech = text.decode('utf-8')
    sess.add(speech)
    sess.commit()
    sess.close()
    
    message.reply(u'わかりました。')

@default_reply
def talk(message):
    sess = Session()
    msgs = sess.query(Speech).count()
    if msgs == 0:
        message.reply(u'あなたに言うことは何もありません。')
        sess.close()
        return

    rand = random.randrange(0, msgs)
    row = sess.query(Speech)[rand]
    speech = row.speech
    sess.close()
    message.reply(speech)
