import json
import os.path
from manageapp import app


def read_user():
    with open(os.path.join(app.root_path, 'data/user.json'), encodings='utf-8') as f:
        return json.load(f)
