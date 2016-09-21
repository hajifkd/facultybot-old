# coding: utf-8

from slackbot.bot import respond_to, default_reply
from .models import Session, Speech, Faculty, NickName
import random
import shlex
import functools

def shlex_args(func):
    @functools.wraps(func)
    def wrapper(message, arg):
        args = shlex.split(arg)
        if len(args) < 2:
            message.reply(u'引数が足りないです')
            return

        args_utf8 = [a.decode('utf-8') for a in args]
        func(message, *args_utf8)
    return wrapper

@respond_to(ur'help')
def help(message):
    message.reply(u''' Facultybot - IPMU名言集

Facultybotは、IPMU周辺の人々の名言を記録するためのbotです。
名言を記録するには、まず発言した人を登録しましょう。

人を登録するには、add facultyコマンドを使います。

例:
@facultybot add faculty ほげふが

この際、Unix shell同様のエスケープが効きます。スペースなどが入る場合
有効に活用してください。以下のコマンドでもすべて同様です。

例:
@facultybot add faculty "Hoge Fuga"

同じ人を別の名前で登録してもいいですが、あまり増やしすぎても発言を登録する際に混乱しそうですのでほどほどに。
登録済みの人を表示するには、ls peopleします。
人にはnicknameをつけることができます。ただし、現状表示される名前は一番最初に登録したものに限ります。

例:
@facultybot add nickname ほげふが hoge

ls peopleでnicknameもすべて表示されます。わかりにくいものを登録するのはやめましょう。
最後に、発言を登録するには、add speechコマンドです。

例:
@facultybot add speech hoge "Hello, IPMU!"

IPMU botを活用して楽しいIPMU学生ライフを過ごしましょう!!  ''')

@respond_to(ur'ls people')
def ls_people(message):
    sess = Session()
    message.reply('\n'.join(n.nickname for n in sess.query(NickName)))
    sess.close()

@respond_to(ur'add faculty (.+)')
def add_faculty(message, name):
    sess = Session()
    name = shlex.split(name)[0].decode('utf-8')

    if sess.query(NickName).filter_by(nickname=name).count():
        message.reply(u'その人はすでに存在しています')
        sess.close()
        return

    faculty = Faculty()
    nick = NickName()
    nick.nickname = name
    faculty.nicknames.append(nick)
    sess.add(faculty)
    sess.add(nick)
    sess.commit()
    sess.close()
    
    message.reply(u'追加しました。')

@respond_to(ur'add nickname (.+)')
@shlex_args
def add_nickname(message, name, nick):
    sess = Session()
    if sess.query(NickName).filter_by(nickname=nick).count():
        message.reply(u'その名前はすでに存在しています')
        sess.close()
        return

    try:
        faculty = sess.query(NickName).filter_by(nickname=name).one().faculty
        nickname = NickName()
        nickname.nickname = nick
        nickname.faculty = faculty
        sess.add(nickname)
        sess.commit()
        message.reply(u'追加しました')
    except:
        message.reply(u'その名前のfacultyは存在しません')

    sess.close()


@respond_to(ur'add speech (.+)')
@shlex_args
def check(message, nick, text):
    sess = Session()
    try:
        faculty = sess.query(NickName).filter_by(nickname=nick).one().faculty
        speech = Speech()
        speech.speech = text
        speech.faculty = faculty
        sess.add(speech)
        sess.commit()
        message.reply(u'わかりました')
    except:
        message.reply(u'その名前のfacultyは存在しません')

    sess.close()



@default_reply
def talk(message):
    sess = Session()
    msgs = sess.query(Speech).count()
    if msgs == 0:
        message.reply(u'あなたに言うことはなにもありません')
        sess.close()
        return

    rand = random.randrange(0, msgs)
    row = sess.query(Speech)[rand]
    speech = row.speech
    name = row.faculty.nicknames[0].nickname
    sess.close()
    message.reply(u'\"%s\" - %s' % (speech, name))
