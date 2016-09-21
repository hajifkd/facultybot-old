from pit import Pit

API_TOKEN = Pit.get('seminarbot', {'require': {'tbot': 'slack_token'}})['tbot']
PLUGINS = ['facultybot.plugins']
