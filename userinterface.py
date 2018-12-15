'''
    Handles all the UI logic. Maybe needs refactoring for each specific page.
'''

from datetime import datetime
from random import randint as r

from box import Box

import userdata



def prompt_for_action():
    '''Prompt for action, main loop for program'''
    while True:
        # print(posts)
        print('\n=====\n')
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


def create_account(users):
    '''Create new user'''
    # global signed_in THIS MIGHT NEED TO BE ON?
    username = input('Please enter a new username:\n>\t')
    password = input('Please enter a new password:\n>\t')
    post_count = input('How many posts would you like to see '
                     'on your timeline?:\n>\t')
    user_id = f"{username[0]}{username[-1]}{r(1,999)}"
    _usernames = [user.username for user in userdata.users()]
    if username in _usernames:
        print('Username is already taken.') 
        return False
    signed_in = Box({'username': username,
                     'password': password,
                     'user_id': user_id,
                     'following': [],
                     'ignoring': [],
                     'post_count': int(post_count)})
    users.append(signed_in)
    userdata._save_users(users)
    return signed_in


def sign_in(username, password, users):
    '''Sign in from existing user account'''
    global signed_in
    # username = input('Please enter your username:\n>\t')
    # password = input('Please enter your password:\n>\t')
    for user in users:
        if username == user.username and password == user.password:
            signed_in = user
            print(f"Signed in as: {signed_in.username.title()}")
            return signed_in #Delete after cleaning up main file for sign in?
        else:
            print('Please sign in as a valid user or create a new account!')
            return False


def validate_posts(posts):
    '''Only show posts from unignored users'''
    _posts = []
    for post in reversed(posts):
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


def display_posts(_posts):
    '''How posts are displayed in timeline'''
    # global post_count
    print('-' * 50)
    for post in _posts[:signed_in.post_count]:
        print(f"|\n|{post.username}\n|\t\t{post.text}\n|")
        print(f"|\n|\t\t\t\t\t{post.timestamp[:10]}")
        print('-' * 50)


def timeline(posts):
    '''Display timeline'''
    print('Timeline:')
    _posts = validate_posts(posts)
    display_posts(_posts)


def add_post(text):
    '''Add new post'''
    _max_post_id = max([post.post_id for post in userdata.posts()])
    new_post = {'post_id': str(_max_post_id + 1),
                'text': text,
                'user_id': signed_in.user_id,
                'timestamp': '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now())}
    return Box(new_post)


def users(users):
    '''users page'''
    _users = [(user.username, user.user_id) for user in users]

    following = signed_in.following
    ignoring = signed_in.ignoring
    while True:
        print('\n=====\n')
        for user in _users:
            if user[1] in following:
                print(f'{user[0].title()} (following)')
            elif user[1] in ignoring:
                print(f'{user[0].title()} (ignoring)')
            else:
                print(f'{user[0].title()}')
        print('F. Follow or unfollow user')
        print('I. Ignore or unignore user')
        print('B. Back')
        action = input('Select an action\n\t>>> ').strip().upper()

        if action == 'F':
            selected_user = input('Select a user to follow '
                                  'or unfollow\n\t>>> ').strip().lower()

            if selected_user not in [user[0].lower() for user in _users]:
                print('This user does not exist.')
                break

            selected_user_id = [user[1] for user in _users if
                                selected_user == user[0]][0]

            if selected_user_id in following:
                signed_in.following.remove(selected_user_id)
                print(f'=====\n{selected_user.title()} unfollowed!\n')
            elif selected_user_id in ignoring:
                print('=====\n')
                print('You cannot follow a user you are ignoring. '
                      'Unignore this user before following them.')
            else:
                signed_in.following.append(selected_user_id)
                print(f'=====\nNow following {selected_user.title()}!\n')

        elif action == 'I':
            selected_user = input('Select a user to follow '
                                  'or unfollow\n\t>>> ').strip().lower()

            if selected_user not in [user[0].lower() for user in _users]:
                print('This user does not exist.')
                break

            selected_user_id = [user[1] for user in _users if
                                selected_user == user[0]][0]

            if selected_user_id in following:
                print('=====\n')
                print('You cannot ignore a user you are following. '
                      'Unfollow this user before ignoring them.')
            elif selected_user_id in ignoring:
                signed_in.ignoring.remove(selected_user_id)
                print(f'=====\n{selected_user.title()} unignored!\n')
            else:
                signed_in.ignoring.append(selected_user_id)
                print(f'=====\nNow ignoring {selected_user.title()}!\n')

        elif action == 'B':
            break


def account(signed_in):
    '''account page'''
    # global post_count
    while True:
        print(f'Username: {signed_in.username}')
        print('MORE DATA')
        print('U. Change Username')
        print('P. Change Password')
        print('T. Timeline Post Count')
        print('B. Back')
        action = input('Select an action\n\t>>> ').strip().upper()

        if action == 'P':
            new_password = input('Type a new password\n\t>>> ')
            signed_in.password = new_password
            print('Password Changed!')
        elif action == 'U':
            new_username = input('Type a new username\n\t>>> ')
            signed_in.username = new_username
            print('Username Changed!')
        elif action == 'T':
            post_count = input("Enter the amount of posts "
                               "you'd like to see on your timeline.\n>>> ").strip()
            signed_in.post_count = int(post_count)
        elif action == 'B':
            break
