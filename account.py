from time import sleep

from box import Box

import timeline


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
            print(f"\nSigned in as: {signed_in.username.title()}\n")
            return signed_in
        print('Please sign in as a valid user or create a new account!')
        return False


def new_password_username(parameter, signed_in):
    '''Update username or password for signed in user'''
    new_parameter = input(f'Type a new {parameter}\n\t>>> ')
    if parameter == 'password':
        signed_in.password = new_parameter
    elif parameter == 'username':
        signed_in.username = new_parameter
    print(f'{parameter.title()} Changed!')
    sleep(1)


def account(signed_in, posts_):
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
                print(f'Currently viewing {signed_in.posts_in_timeline}'
                      f' post(s) per page.')
                sleep(1)

            else:
                print('\nYou must enter a number.\n')
                sleep(1)
        elif action == 'M':
            posts_ = [post for post in posts_ if post.user_id == signed_in.user_id]
            timeline.timeline([signed_in], posts_, signed_in, 1)
            sleep(1)
        elif action == 'B':
            break
