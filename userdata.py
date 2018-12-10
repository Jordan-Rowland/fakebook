# from datetime import datetime
# '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now())
import json
from os.path import exists
from random import randint as r
from time import sleep


# users = [
#         {'username': 'jordan', 'password': 'jr11', 'user_id': 'jr123', 'following': ['bm123','fl123',], 'ignoring': ['rb123'],},
#         {'username': 'batman', 'password': 'bw11', 'user_id': 'bm123', 'following': ['jr123','rb123','jk123','fl123','sm123'], 'ignoring': [],},
#         {'username': 'robin', 'password': 'dg11', 'user_id': 'rb123', 'following': ['bm123'], 'ignoring': ['jr123'],},
#         {'username': 'superman', 'password': 'ck11', 'user_id': 'sm123', 'following': ['jr123','fl123'], 'ignoring': ['bm123',],},
#         {'username': 'joker', 'password': 'jv11', 'user_id': 'jk123', 'following': ['bm123',], 'ignoring': ['jr123', 'bm123','rb123','sm123','fl123',],},
#         {'username': 'flash', 'password': 'ba11', 'user_id': 'fl123', 'following': ['bm123','rb123','sm123',], 'ignoring': [],}
#          ]


def init():
    _load_posts()
    _load_users()


def create_account():
    global signed_in
    username = input('Please enter a new username:\n>\t')
    password = input('Please enter a new password:\n>\t')
    user_id = f"{username[0]}{username[-1]}{r(1,999)}"
    for user in users:
        if username == user['username']:
            print('Username is already taken.')
            return False
    users.append({'username': username, 'password': password, 'user_id': user_id, 'following': [], 'ignoring': []})
    signed_in = {'username': username, 'password': password, 'user_id': user_id, 'following': [], 'ignoring': []}
    _save_users()
    _load_users()
    return True


def sign_in():
    global signed_in
    username = input('Please enter your username:\n>\t')
    password = input('Please enter your password:\n>\t')
    for user in users:
        if username == user['username'] and password == user['password']:
            signed_in = user
            print(f"Signed in as: {signed_in['username'].title()}")
            return True
        else:
            print('Please sign in as a valid user or create a new account!')
            return False


def landing(username,password,users):
    global signed_in
    signed_in = ''


# Need to assign username 
def validate_posts(posts):
    global _posts
    _posts = []
    for post in posts[::-1]:
        if post['user_id'] in signed_in['ignoring']:
            continue
        for user in users:
            if post['user_id'] == user['user_id']:
                if user['user_id'] in signed_in['following']:
                    username = f"*{user['username'].title()}"
                    break
                elif post['user_id'] == user['user_id']:
                    username = user['username'].title()
                    break
        text = post['text']
        _posts.append({'username': username, 'text': text, 'post_id': post['user_id']})
    return _posts


def display_posts():
    global _posts
    print('-' * 50)
    for post in _posts:
        print(f"|\n|\n|{post['username']}\n|\t{post['text']}\n|\n|")
        print('-' * 50)


def timeline():
    print('Timeline:')
    _load_users()
    validate_posts(posts)
    display_posts()


def _load_posts():
    '''
         If file exists, read from file. Else, initiate empty list as items
    '''
    global posts
    if exists('posts.json'):
        with open('posts.json','r') as file:
            posts = json.loads(file.read())
    else:
        posts = [
# {'post_id': '1',
#   'text': 'Got here before anyone!',
#   'user_id': 'fl123',
#   'timestamp': '2018-05-10 04:21:02'},
#  {'post_id': '2',
#   'text': 'Shut up Barry',
#   'user_id': 'bm123',
#   'timestamp': '2018-06-10 04:21:07'},
#  {'post_id': '3',
#   'text': 'LOL',
#   'user_id': 'rb123',
#   'timestamp': '2018-07-10 04:21:12'},
#  {'post_id': '4',
#   'text': 'HahahahHAHAha ha HAHA',
#   'user_id': 'jk123',
#   'timestamp': '2018-08-07 04:21:17'},
#  {'post_id': '5',
#   'text': 'fuck bitches',
#   'user_id': 'jr123',
#   'timestamp': '2018-08-10 04:21:22'},
#  {'post_id': '6',
#   'text': 'Anyone seen lois?',
#   'user_id': 'sm123',
#   'timestamp': '2018-09-02 04:21:27'},
#  {'post_id': '7',
#   'text': 'See you in Bludhaven',
#   'user_id': 'rb123',
#   'timestamp': '2018-10-10 04:21:32'},
#  {'post_id': '8',
#   'text': 'So Fast!',
#   'user_id': 'fl123',
#   'timestamp': '2018-11-05 04:21:37'},
#  {'post_id': '9',
#   'text': 'SHUT UP BARRY',
#   'user_id': 'bm123',
#   'timestamp': '2018-11-13 04:21:42'},
#  {'post_id': '10',
#   'text': 'your mom!',
#   'user_id': 'jr123',
#   'timestamp': '2018-11-10 04:21:47'}
        ]


def _save_posts():
    '''
        Save posts list to File
    '''
    global posts
    with open('posts.json','w') as file:
        file.write(json.dumps(posts))


def _load_users():
    '''
         If file exists, read from file. Else, initiate empty list as items
    '''
    global users
    if exists('users.json'):
        with open('users.json','r') as file:
            users = json.loads(file.read())
    else:
        users = []


def _save_users():
    '''
        Save users list to File
    '''
    global users
    with open('users.json','w') as file:
        file.write(json.dumps(users))