"""Module to handle everything related to user account"""

from random import randint as r
import sys
from time import sleep

from box import Box

import userdata
import userinterface


def verify_username(database_connection, username, new_user):
    """Verify username for new or existing users"""
    existing_usernames = (user[1] for user in
                          userdata.user_data_iter(
                              database_connection))

    if new_user:
        if username in existing_usernames:
            print('Username already exists.')
            return False
        return True
    return username in existing_usernames


def ask_and_verify_username(database_connection, new_user=False):
    """Ask for a verify user on log in or account creation"""
    username = userinterface.ask_for(f'Please enter a username.')
    username_verified = verify_username(database_connection,
                                        username, new_user)
    if not username_verified:
        return False
    return username


def generate_user_id(username):
    """Generate new user ID for user based on username
    and random characters"""
    return f'{username[0]}{username[-1]}{r(1000,99999)}'


def verify_new_password(password):
    """Verify password strength"""
    has_upper_char = any(x.isupper() for x in password)
    has_lower_char = any(x.islower() for x in password)
    has_digit_char = any(x.isdigit() for x in password)
    long_enough = len(password) > 8

    if has_upper_char and has_lower_char and has_digit_char and long_enough:
        return True

    print('Password not strong enough!')
    return False


def ask_and_verify_password():
    """Ask new user for password and verify password is
    strong enough"""
    password = userinterface.ask_for('Please enter a new password.')
    password_verified = verify_new_password(password)
    if not password_verified:
        return False
    return password


def ask_timeline_preferences():
    """Ask user how many posts they would like to see per page"""
    print('How many posts would you like to see per page?')
    posts_in_timeline = input('\t==> ')
    try:
        return int(posts_in_timeline)
    except ValueError:
        return False


def verify_number(number):
    """Verify input os a number"""
    if isinstance(number, int):
        return True
    print('\nYou must enter a number.\n')
    return False


# def ask_and_verify_timeline_preferences():
#     """Ask for timeline post count, and verify input is a number"""
#     post_number = ask_timeline_preferences()
#     post_number_verified = verify_number(post_number)

#     if not post_number_verified:
#         print('You must enter a number!')
#         return False
#     return post_number


def validate_user_sign_in(database_connection, username, password):
    """Check user information against database"""
    if not username:
        return False
    cursor = database_connection.cursor()
    query = cursor.execute('''SELECT * FROM users
                              WHERE username = ?
                              AND password = ?''',
                           (username.lower(), password, ))
    user = [Box(dict(row)) for row in query]
    if user:
        signed_in = user[0]
        print(f'\nSigned in as: {signed_in.username.title()}\n')
        cursor.close()
        return signed_in
    return False


def confirm_new_user_added_to_database(user_data, database_connection,
                                       username, password):
    """Confirms entering new user to database, and return
    signed in user instance"""
    creation_success = userdata.insert_new_user(
        database_connection, user_data)
    if not creation_success:
        return False

    signed_in = validate_user_sign_in(database_connection,
                                      username, password)
    return signed_in


def create_account(database_connection):
    """Create a new user account"""
    username  = ask_and_verify_username(database_connection, new_user=True)
    if not username:
        return False
    password = ask_and_verify_password()
    if not password:
        return False
    user_id = generate_user_id(username)
    location = userinterface.ask_for('Please enter your location')
    # post_number = ask_and_verify_timeline_preferences()

    user_data = (user_id, username, password,
                 location, 6)
    if not all(user_data):
        print('Something went wrong! Unable to create account.')
        return False
    return confirm_new_user_added_to_database(user_data, database_connection,
                                              username, password)



###### REMOVE USERNAME AND PASSWORD ARGUMENTS WHEN DONE TESTING
# def sign_in(username, password, database_connection):
def sign_in(database_connection):
    """Sign in from existing user account"""
    username  = ask_and_verify_username(database_connection, new_user=False)
    if not username:
        print('Username does not exist')
        return False
    password = userinterface.ask_for('Please enter your password.')
    signed_in = validate_user_sign_in(database_connection,
                                      username, password)
    if not signed_in:
        print('Password incorrect!')
        return False
    return signed_in


def sign_in_or_create_user(database_connection):
    """First prompting function in main function to sign in
    as existing user, or create new user"""
    while True:
        print('Press (N) to create a new account or (S) to '
              'sign into an existing account. Press (X) to exit.')
        action = input('\t==> ').strip().upper()
        if action == 'N':
            signed_in = create_account(database_connection)
            if signed_in:
                return signed_in
            continue
        elif action == 'S':
            signed_in = sign_in(database_connection)
            if signed_in:
                return signed_in
            continue
        elif action == 'X':
            print('Bye!')
            sys.exit()
        print('Not a valid operation')


def verify_existing_password_for_update(signed_in):
    """Ask user for password to verify"""
    old_password_on_file = signed_in.password
    check_password = userinterface.ask_for('Please enter your current password')
    same_password = old_password_on_file == check_password
    if not same_password:
        print('Incorrect password.')
        return False
    return True


def new_password_setup(database_connection, signed_in):
    """Change the users password"""
    if verify_existing_password_for_update(signed_in):
        new_password = userinterface.ask_for('Please enter a new password')
        password_verified = verify_new_password(new_password)
        if password_verified:
            userdata.set_new_password(database_connection, signed_in,
                                      new_password=new_password)
            signed_in.password = new_password
            print('Password changed!')



def new_username_setup(database_connection, signed_in):
    """Change the users username"""
    print(f'Current username: {signed_in.username}')
    new_username = userinterface.ask_for('Please enter a new username')
    userdata.set_new_username(database_connection, signed_in, new_username=new_username)
    signed_in.username = new_username
    print('Username changed!')


def new_password_or_username(parameter, database_connection, signed_in):
    """Update username or password for signed in user"""
    if parameter == 'password':
        new_password_setup(database_connection, signed_in)
    elif parameter == 'username':
        new_username_setup(database_connection, signed_in)
    sleep(1)


def update_new_timeline_view(database_connection,
                             post_number,
                             signed_in):
    """Change post count in timeline"""
    cursor = database_connection.cursor()
    cursor.execute('''UPDATE users
                      SET posts_per_page = ?
                      WHERE user_id = ?;''',
                   (post_number, signed_in.user_id))

    signed_in.posts_per_page = post_number
    print(f'Currently viewing {signed_in.posts_per_page}'
          f' post(s) per page.')
    sleep(1)


def timeline_view_preferences(database_connection, signed_in):
    """Update posts per page on timeline"""
    print(f'Currently viewing {signed_in.posts_per_page} post(s) per page.')
    sleep(1)

    post_number = ask_timeline_preferences()
    post_number_verified = verify_number(post_number)

    if post_number_verified:
        update_new_timeline_view(database_connection, post_number, signed_in)


def view_self_posts(database_connection, signed_in,):
    """View signed in users posts in Account section"""
    while True:
        query = userdata.return_self_posts(database_connection, signed_in)
        userinterface.display_posts(query, database_connection, signed_in,
                                    page_num=1, post_id_show=True)
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
            timeline_view_preferences(database_connection, signed_in)
        elif action == 'M':
            view_self_posts(database_connection, signed_in,)
        elif action == 'B':
            break
