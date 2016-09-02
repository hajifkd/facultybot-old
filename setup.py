try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Taizanbot',
    'author': 'Hajime Fukuda',
    'url': 'http://member.ipmu.jp/hajime.fukuda/',
    'author_email': 'hajime.fukuda@ipmu.jp',
    'version': '0.1',
    'install_requires': ['slackbot', 'pit', 'sqlalchemy'],
    'packages': ['taizanbot'],
    'name': 'taizanbot',
}

setup(**config)
