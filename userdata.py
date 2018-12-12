import json
from os.path import exists
from box import Box


def init():
    '''
        Initiate posts andusers
    '''
    users = _load_users()
    posts = _load_posts()
    return [Box(user) for user in users], [Box(post) for post in posts]
    # return users, posts



def _load_posts():
    '''
         If file exists, read from file. Else, initiate empty list as items
    '''
    # global posts
    if exists('posts.json'):
        with open('posts.json', 'r') as file:
            posts = json.loads(file.read())
    else:
        posts = []
    return posts


def _save_posts(posts):
    '''
        Save posts list to File
    '''
    # global posts
    with open('posts.json', 'w') as file:
        file.write(json.dumps(posts))


def _load_users():
    '''
         If file exists, read from file. Else, initiate empty list as items
    '''
    # global users
    if exists('users.json'):
        with open('users.json', 'r') as file:
            users = json.loads(file.read())
    else:
        users = []
    return users


def _save_users(users):
    '''
        Save users list to File
    '''
    # global users
    with open('users.json', 'w') as file:
        file.write(json.dumps(users))
