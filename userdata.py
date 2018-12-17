'''
    All data logic is here
'''


import json
from os.path import exists

from box import Box


def init():
    '''
        Initiate posts and users
    '''
    _users = _load_users()
    _posts = _load_posts()
    _users = [Box(user) for user in _users]
    _posts = [Box(post) for post in _posts]

    return _users, _posts


def _load_posts():
    '''
         If file exists, read from file. Else, initiate empty list as items
    '''
    if exists('fakebook/posts.json'):
        with open('fakebook/posts.json', 'r') as file:
            _posts = json.loads(file.read())
    else:
        _posts = []
    return _posts


def save_posts(posts):
    '''
        Save posts list to File
    '''
    with open('fakebook/posts.json', 'w') as file:
        file.write(json.dumps(posts, indent=4, sort_keys=True))


def _load_users():
    '''
         If file exists, read from file. Else, initiate empty list as items
    '''
    if exists('fakebook/users.json'):
        with open('fakebook/users.json', 'r') as file:
            _users = json.loads(file.read())
    else:
        # _users = []
        _users = [{"username": "Jordan00", "password": "jr11", "user_id": "jr123", "following": ["bm123", "fl123"], "ignoring": ["rb123"]}, {"username": "batman", "password": "bw11", "user_id": "bm123", "following": ["jr123", "rb123", "jk123", "fl123", "sm123"], "ignoring": []}, {"username": "robin", "password": "dg11", "user_id": "rb123", "following": ["bm123"], "ignoring": ["jr123"]}, {"username": "superman", "password": "ck11", "user_id": "sm123", "following": ["jr123", "fl123"], "ignoring": ["bm123"]}, {"username": "joker", "password": "jv11", "user_id": "jk123", "following": ["bm123"], "ignoring": ["jr123", "bm123", "rb123", "sm123", "fl123"]}, {"username": "flash", "password": "ba11", "user_id": "fl123", "following": ["bm123", "rb123", "sm123"], "ignoring": []}]

    return _users


def save_users(users):
    '''
        Save users list to File
    '''
    with open('fakebook/users.json', 'w') as file:
        file.write(json.dumps(users, indent=4, sort_keys=True))
