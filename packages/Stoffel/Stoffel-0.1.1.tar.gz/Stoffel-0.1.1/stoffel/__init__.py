from stoffel.settings import *
import os
import json

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if not os.path.isfile(CONNECTIONS_PATH):
    with open(CONNECTIONS_PATH, 'w+') as f:
        json.dump({}, f, indent=4)