'''Module to handle everything related to user account'''

from random import randint as r
from time import sleep

from box import Box

import timeline
import userdata


def ask_for(message):
    print(f'{message}')
    username = input('\t==> ').strip()
    return username


def verify_username(database_connection, username, new_user=False):
    existing_usernames = (user[1] for user in
                          userdata.user_iter(
                            database_connection))

    if new_user:
        if username in existing_usernames:
            print('Username already exists.')
            return False
        return True
    else:
        return username in existing_usernames


def verify_password(password):
    if not any(x.isupper() for x in password)\
    or not any(x.islower() for x in password)\
    or not any(x.isdigit() for x in password)\
    or len(password) < 8:
        print('Password not strong enough!')
        return False
    return True


def ask_timeline_preferences():
    print('How many posts would you like to see per page?')
    posts_in_timeline = input('\t==> ')
    try:
        return int(posts_in_timeline)
    except ValueError:
        return False


def verify_number(number):
    if isinstance(number, int):
        return True
    print('\nYou must enter a number.\n')
    return False


def validate_user_sign_in(database_connection, username, password):
    """Check user information against database"""
    cursor = database_connection.cursor()
    query = cursor.execute('''SELECT * FROM users
                            WHERE username = ?
                            AND password = ?''',
                      (username, password, ))

    query_list = list(query)
    if query_list:
        signed_in = [Box(dict(row)) for row in query_list][0]
        print(f'\nSigned in as: {signed_in.username.title()}\n')
        cursor.close()
        return signed_in
    else:
        return False


def validate_new_user_data(user_data):
    creation_success = userdata.insert_new_user(
                                  database_connection, user_data)
    if not creation_success:
        return False

    signed_in = validate_user_sign_in(database_connection,
                                      username, password)
    return signed_in



def create_account(database_connection):
    """Create a new user account"""
    username = ask_for('Please enter a new username.')
    username_verified = verify_username(database_connection,
                                        username, new_user=True)
    if not username_verified:
        return False

    password = ask_for('Please enter a new password.')
    password_verified = verify_password(password)
    if not password_verified:
        return False

    location = ask_for('Please enter your location')

    post_preference_number = ask_timeline_preferences()
    post_preference_number_verified = verify_number(
                                        post_preference_number)

    if not post_preference_number_verified:
        return False

    user_id = f'{username[0]}{username[-1]}{r(1000,99999)}' # Create user ID

    user_data = (user_id, username, password,
                 location, post_preference_number)

    if all(user_data):
        return validate_new_user_data(user_data)

    print('Something went wrong! Unable to create account.')
    return False


###### REMOVE USERNAME AND PASSWORD ARGUMENTS WHEN DONE TESTING
def sign_in(username, password, database_connection):
# def sign_in(database_connection):
    # """Sign in from existing user account"""
    # username = ask_for('Please enter your username.')
    # username_verified = verify_username(database_connection, username)
    # if not username_verified:
    #     print('This username does not exist!')
    #     return False

    # password = ask_for('Please enter your password.')

    signed_in = validate_user_sign_in(database_connection,
                                      username, password)
    if signed_in:
        return signed_in

    print('Password incorrect!')
    return False


def verify_existing_password_for_change(signed_in):
    """Ask user for password to verify"""
    old_password_on_file = signed_in.password
    check_password = ask_for('Please enter your current password')
    same_password = old_password_on_file == check_password
    if not same_password:
        print('Incorrect password.')
        return False

    return True


def new_password_set_up(database_connection, signed_in):
    """Change the users password"""
    if verify_existing_password_for_change(signed_in):
        new_password = ask_for('Please enter a new password')
        password_verified = verify_password(new_password)
        if not password_verified:
            return False

        userdata.set_new_password(database_connection, signed_in, new_password=new_password)
        signed_in.password = new_password


def new_username_set_up(database_connection, signed_in):
    """Change the users username"""
    print(f'Current username: {signed_in.username}')
    new_username = ask_for('Please enter a new username')
    userdata.set_new_username(database_connection, signed_in, new_username=new_username)
    signed_in.username = new_username
    print('Username changed!')


def new_password_or_username(parameter, database_connection, signed_in):
    """Update username or password for signed in user"""
    if parameter == 'password':
        new_password_setup(database_connection, signed_in)

    elif parameter == 'username':
        new_username_set_up(database_connection, signed_in)

    database_connection.commit()
    sleep(1)


def update_new_timeline_view(database_connection, posts):
    """Change post count in timeline"""
    cursor = database_connection.cursor()
    cursor.execute('''UPDATE users
                 SET posts_per_page = ?
                 WHERE user_id = ?;''',
              (post_preference_number, signed_in.user_id))

    signed_in.posts_per_page = post_preference_number
    print(f'Currently viewing {signed_in.posts_per_page}'
          f' post(s) per page.')
    sleep(1)


def timeline_view(database_connection, signed_in):
    """Update posts per page on timeline"""
    print(f'Currently viewing {signed_in.posts_per_page} post(s) per page.')
    sleep(1)

    post_number = ask_timeline_preferences()
    post_number_verified = verify_number(post_preference_number)

    if post_number_verified:
        update_new_timeline_view(database_connection, post_number)


def view_self_posts(database_connection, signed_in,):
    while True:
        query = userdata.return_self_posts(database_connection, signed_in)

        timeline.display_posts(query, database_connection, signed_in,
                               1, post_id_show=True)

        print('(D) Delete Post')
        print('(B) Back')
        post_action = input('\n\t==> ').strip().upper()

        if post_action == 'B':
            break
        elif post_action == 'D':
            print('Enter the ID of the post you would like to delete')
            input_post_id = input('\n\t==> ')
            userdata.remove_post(database_connection,
                        signed_in, int(input_post_id))


def account(signed_in, database_connection):
    """Account page"""
    while True:
        print('\n')
        print(f'Username: {signed_in.username.title()} - {signed_in.location}')
        print('\n')
        print('> (U) Change Username')
        print('> (P) Change Password')
        print('> (T) Timeline Post Count')
        print('> (M) My Recent Posts')
        print('> (B) Back')
        action = input('Select an action\n\t==> ').strip().upper()

        if action == 'U':
            new_password_or_username('username', database_connection, signed_in)
        elif action == 'P':
            new_password_or_username('password', database_connection, signed_in)
        elif action == 'T':
            timeline_view(database_connection, signed_in)
        elif action == 'M':
            view_self_posts(database_connection, signed_in,)
        elif action == 'B':
            break
