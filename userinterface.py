'''
    Handles all the UI logic. Maybe needs refactoring for each specific page.
'''

from datetime import datetime
from random import randint as r
from time import sleep

from box import Box

import userdata


def prompt_for_action():
    '''Prompt for action, main loop for program'''
    while True:
        print('\n=====\n')
        print('> (#) Timeline Page')
        print('> (A) Account')
        print('> (U) Users')
        print('> (P) Post')
        print('> (O) Sign Out')
        action = input('Select an action\n\t>>> ').strip().upper()

        options = {'A': 'ACCOUNT SETTINGS',
                   'U': 'USERS',
                   'P': 'POST',
                   'O': 'SIGN OUT'}

        if action.isdigit():
            return action
        if action in options.keys():
            return options[action]
        continue


def create_account(users_):
    '''Create new user'''
    username = input('Please enter a new username:\n>\t')
    _usernames = [user.username for user in users_]
    if username in _usernames: # check if username is taken
        print('Username is already taken.')
        return False
    password = input('Please enter a new password:\n>\t')
    if not any(x.isupper for x in password) or not any(x.islower for x in password)\
    or not any(x.isdigit for x in password) or len(password) < 8: # Validate password
        print('Invalid password')
        return False
    location = input('Enter your location:\n>\t')
    print('How many posts would you like to see')
    posts_in_timeline = input('\t>>> ')

    user_id = f"{username[0]}{username[-1]}{r(1,999)}" # create user ID
    signed_in = Box({'username': username,
                     'password': password,
                     'user_id': user_id,
                     'location': location,
                     'following': [],
                     'ignoring': [],
                     'posts_in_timeline': int(posts_in_timeline)})
    users_.append(signed_in)
    userdata.save_users(users_)
    return signed_in

###### REMOVE USERNAME AND PASSWORD ARGUMENTS WHEN DONE TESTING
def sign_in(username, password, users_):
    '''Sign in from existing user account'''
    # username = input('Please enter your username:\n>\t')
    # password = input('Please enter your password:\n>\t')
    for user in users_:
        if username == user.username and password == user.password:
            signed_in = user
            print(f"Signed in as: {signed_in.username.title()}")
            return signed_in
        print('Please sign in as a valid user or create a new account!')
        return False

### TIMELINE
def validate_posts(posts, users_, signed_in):
    '''Only show posts from unignored users'''
    _posts = []
    for post in reversed(sorted(posts, key=lambda k: k['post_id'])):
        if post.user_id in signed_in.ignoring:
            continue
        for user in users_:
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


def display_posts(_posts, signed_in, page_num):
    '''How posts are displayed in timeline'''
    start_post = signed_in.posts_in_timeline * (page_num - 1)
    end_post = signed_in.posts_in_timeline * page_num
    print('-' * 50)
    _posts = _posts[start_post:end_post]
    if not _posts:
        print(f'No posts on page {page_num}. Please go back a page.')
    else:
        for post in _posts:
            print(f"|\n|{post.username}\n|\t\t{post.text}\n|")
            print(f"|\n|\t\t\t\t\t{post.timestamp[:10]}")
            print('-' * 50)


def timeline(users_, posts, signed_in, page_num):
    '''Display timeline'''
    print(f'Timeline: page {page_num}')
    _posts = validate_posts(posts, users_, signed_in)
    display_posts(_posts, signed_in, page_num)

### ADD POST
def add_post(text, posts, signed_in):
    '''Add new post'''
    _max_post_id = max([post.post_id for post in posts])
    new_post = {'post_id': _max_post_id + 1,
                'text': text,
                'user_id': signed_in.user_id,
                'timestamp': '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now())}
    return Box(new_post)

### USERS PAGE
def display_users(users_, following, ignoring):
    '''Display users and user relations'''
    print('\n=====\n')
    for user in users_:
        if user.user_id in following:
            print(f'{user.username.title()} (following)')
        elif user.user_id in ignoring:
            print(f'{user.username.title()} (ignoring)')
        else:
            print(f'{user.username.title()}')
    print('\n=====\n')
    sleep(1)


def validate_user(users_, selected_user):
    '''Check for valid selected user'''
    if selected_user.lower() in [user.username.lower() for user in users_]:
        return True
    print('This user does not exist.')
    sleep(1)
    return False


def select_user(users_, action):
    prompt_for_user = print(f'Select the user you would like to '
        f'{action} or un{action}')
    selected_user = input('\t>>> ').strip().lower()
    if validate_user(users_, selected_user):
        user = [user for user in users_ if selected_user == user.username][0]
        return user
    return False


def add_remove_user(user, list_, second_list_, action):
    '''Add or remove user from follow or ignore list'''
    if user.user_id in second_list_:
        print('User cannot be ignored and followed at the same time.\n'
              'Remove this user from one of these lists to continue. ')
    elif user.user_id in list_:
        list_.remove(user.user_id)
        print(f'=====\nNow un{action[:-1] if action.endswith("e") else action}ing '
              f'{user.username.title()}.')
    else:
        list_.append(user.user_id)
        print(f'=====\nNow {action[:-1] if action.endswith("e") else action}ing '
              f'{user.username.title()}.')
    sleep(1)


def follow_or_ignore(users_, list_, second_list_, action):
    '''Over all meta-function for following, ignoring'''
    user = select_user(users_, action)
    if user:
        add_remove_user(user, list_, second_list_, action)


#######################################################
#####       TEST REFACTOR       #####
#######################################################


def prompt_for_user_profile(users_):
    '''Return a profile for any user'''
    print('Enter the username of the user you would like to view')
    username = input('\t>>> ')
    if validate_user(users_, username):
        user = [user for user in users_ if username.lower() == user.username.lower()][0]
        user_following = [friend.username for friend in users_
                     if friend.user_id in user.following]
        user_ignoring = [friend.username for friend in users_
                    if friend.user_id in user.ignoring]
        return user, user_following, user_ignoring


# in Whie loop
def displey_user_profile(signed_in, user, user_following, user_ignoring):
    print('\n=====\n')
    if user.user_id in signed_in.following:
        print(f'Username: {user.username.title()} - Following')
    elif user.user_id in signed_in.ignoring:
        print(f'Username: {user.username.title()} - Ignoring')
    else:
        print(f'Username: {user.username.title()}')

    print(f'Location: {user.location}\n')
    print(f'Bio: {user.biography}')
    print('Following: ')
    if following:
        for followed_user in following:
            print(f'\t{followed_user.title()}')
    else:
        print('\tNot following any users.')
    print('Ignoring: ')
    if ignoring:
        for followed_user in ignoring:
            print(f'\t{followed_user.title()}')
    else:
        print('\tNot ignoring any users')

# in Whie loop
def prompt_for_profile_action(user, signed_in):
    '''Return a profile for any user'''
    print('(F) Follow or unfollow this user')
    print('(I) Ignore or unignore this user')
    print('(B) Back')
    print(user.username.title())
    action = input('>>> ').strip().upper()

    if action == 'B':
        return

    elif action == 'F':
        add_remove_user(user.user_id, signed_in.following,
                        signed_in.ignoring, user.username, 'follow')

    elif action == 'I':
        add_remove_user(user.user_id, signed_in.ignoring,
                        signed_in.following, user.username, 'ignore')


def user_profile(users, signed_in):
    user, user_following, user_ignoring = prompt_for_user_profile(users_)
    while True:
        displey_user_profile(signed_in, user, user_following, user_ignoring)
        prompt_for_profile_action(user, signed_in)


#######################################################
#####       END TEST REFACTOR
#######################################################


def users_page(users_, signed_in):
    '''users page'''
    while True:
        display_users(users_, signed_in.following, signed_in.ignoring)
        print('(P) View users profile')
        print('(F) Follow or unfollow user')
        print('(I) Ignore or unignore user')
        print('(B) Back')
        print('Select an action')
        action = input('\t>>> ').strip().upper()

        if action == 'B':
            break

        elif action == 'P':
            user_profile(users_, signed_in)

        elif action == 'F':
            follow_or_ignore(users_, signed_in.following, signed_in.ignoring, 'follow')

        elif action == 'I':
            follow_or_ignore(users_, signed_in.ignoring, signed_in.following, 'ignore')

        else:
            print('Please enter a valid option')


### ACCOUNT
def new_password_username(parameter, signed_in):
    '''Update username or password for signed in user'''
    new_parameter = input(f'Type a new {parameter}\n\t>>> ')
    if parameter == 'password':
        signed_in.password = new_parameter
    elif parameter == 'username':
        signed_in.username = new_parameter
    print(f'{parameter.title()} Changed!')
    sleep(1)


def account(signed_in, posts):
    '''account page'''
    while True:
        print(f'Username: {signed_in.username} - {signed_in.location}')
        print('(U) Change Username')
        print('(P) Change Password')
        print('(T) Timeline Post Count')
        print('(M) My Recent Posts')
        print('(B) Back')
        action = input('Select an action\n\t>>> ').strip().upper()

        if action == 'P':
            new_password_username('password', signed_in)
        elif action == 'U':
            new_password_username('username', signed_in)
        elif action == 'T':
            print(f'Currently viewing {signed_in.posts_in_timeline} post(s) per page.')
            sleep(1)
            print("Enter the amount of posts you'd like to see on your "
                  "timeline(Please enter a positive integer value).")
            posts_in_timeline = input('\n>>> ').strip()

            if posts_in_timeline.isdigit():
                signed_in.posts_in_timeline = int(posts_in_timeline)
            else:
                print('\nYou must enter a number.\n')
                sleep(1)
        elif action == 'M':
            _posts = [post for post in posts if post.user_id == signed_in.user_id]
            timeline([signed_in], _posts, signed_in, 1)
            sleep(1)
        elif action == 'B':
            break


# def account_page
    #while True:
        # def prompt_for_account_settings
        # def show_own_posts
