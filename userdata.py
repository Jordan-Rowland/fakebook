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
        _users = []
    return _users


def save_users(users):
    '''
        Save users list to File
    '''
    with open('fakebook/users.json', 'w') as file:
        file.write(json.dumps(users, indent=4, sort_keys=True))
