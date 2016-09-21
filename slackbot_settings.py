from pit import Pit

API_TOKEN = Pit.get('seminarbot', {'require': {'fbot': 'slack_token'}})['fbot']
PLUGINS = ['facultybot.plugins']
