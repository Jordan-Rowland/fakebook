from datetime import datetime
from random import randint as r

from box import Box

import userdata



def prompt_for_action():
    while True:
        # print(posts)
        print('> T. Timeline')
        print('> A. Account')
        print('> U. Users')
        print('> P. Post')
        print('> O. Sign Out')
        action = input('Select an action\n\t>>> ').strip().upper()
        # users = userdata.users()
        # posts = userdata.posts()

        if action == 'T': return 'TIMELINE'
        elif action == 'A': return 'ACCOUNT'
        elif action == 'U': return 'USERS'
        elif action == 'P': return 'POST'
        elif action == 'O': return 'SIGN OUT'
        else:
            continue


def create_account():
    global signed_in
    username = input('Please enter a new username:\n>\t')
    password = input('Please enter a new password:\n>\t')
    user_id = f"{username[0]}{username[-1]}{r(1,999)}"
    _usernames = [user.username for user in userdata.users()]
    if username in _usernames:
        print('Username is already taken.')
        return False
    signed_in = Box({'username': username,
                     'password': password,
                     'user_id': user_id,
                     'following': [],
                     'ignoring': []})
    users.append(signed_in)
    userdata._save_users()
    return signed_in


def sign_in(username, password):
    global signed_in
    # username = input('Please enter your username:\n>\t')
    # password = input('Please enter your password:\n>\t')
    for user in userdata.users():
        if username == user.username and password == user.password:
            signed_in = user
            print(f"Signed in as: {signed_in.username.title()}")
            return signed_in
        else:
            print('Please sign in as a valid user or create a new account!')
            return False


def validate_posts(posts):
    _posts = []
    for post in posts[::-1]:
        if post.user_id in signed_in.ignoring:
            continue
        for user in userdata.users():
            if post.user_id == user.user_id:
                if user.user_id in signed_in.following:
                    username = f"*{user.username.title()}"
                    break
                elif post.user_id == user.user_id:
                    username = user.username.title()
                    break
        _posts.append(Box({'username': username,
                           'text': post.text,
                           'post_id': post.user_id,
                           'timestamp': post.timestamp
                           }))
    return _posts


def display_posts(_posts,page):
    print('-' * 50)
    first_post = 1
    last_post = 6
    for post in _posts[(first_post * page) - 1:(last_post * page) - 1]:
        print(f"|\n|{post.username}\n|\t\t{post.text}\n|")
        print(f"|\n|\t\t\t\t\t{post.timestamp[:10]}")
        print('-' * 50)


def timeline(posts):
    print('Timeline:')
    _posts = validate_posts(posts)
    display_posts(_posts,1)


def add_post(text):
    # global signed_in
    _max_post_id = max([int(post.post_id) for post in userdata.posts()])
    new_post = {'post_id': str(_max_post_id + 1),
                'text': text,
                'user_id': signed_in['user_id'],
                'timestamp': '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now())}
    return Box(new_post)


def users(users):
    _users = [(user.username, user.user_id) for user in users]
    print(_users)
    # follow, ignore
    

def account(signed_in):
    print(signed_in)
    # change password, change username