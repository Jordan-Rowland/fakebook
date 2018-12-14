import json
from os.path import exists

from box import Box


def init():
    '''
        Initiate posts and users
    '''
    _load_users()
    _load_posts()


def users():
    global _users
    return [Box(user) for user in _users]


def posts():
    global _posts
    return [Box(post) for post in _posts]


def _load_posts():
    '''
         If file exists, read from file. Else, initiate empty list as items
    '''
    global _posts
    if exists('fakebook/posts.json'):
        with open('fakebook/posts.json', 'r') as file:
            _posts = json.loads(file.read())
    else:
        _posts = []
    return _posts


def _save_posts(posts):
    '''
        Save posts list to File
    '''
    # global posts
    with open('fakebook/posts.json', 'w') as file:
        file.write(json.dumps(posts))


def _load_users():
    '''
         If file exists, read from file. Else, initiate empty list as items
    '''
    global _users
    if exists('fakebook/users.json'):
        with open('fakebook/users.json', 'r') as file:
            _users = json.loads(file.read())
    else:
        _users = []
    return _users


def _save_users(users):
    '''
        Save users list to File
    '''
    # global users
    with open('fakebook/users.json', 'w') as file:
        file.write(json.dumps(users))
