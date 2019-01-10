"""Module to handle Users page and user connections"""

from time import sleep

from box import Box

import userinterface
import userdata


def display_no_users_on_page(page_num):
    """Display on pages with no posts"""
    print('-' * 50)
    print(f'No users on page {page_num}. Please go back a page.')
    print('-' * 50)


def display_users_and_relations(query, following_list, ignoring_list):
    """Tell signed in user if other users on user page are being
    followed or ignored by their account"""
    print('\n=====\n')
    for user in query:
        user = Box(dict(user))
        if user.user_id in following_list:
            print(f'{user.username.title()} (following)')
        elif user.user_id in ignoring_list:
            print(f'{user.username.title()} (ignoring)')
        else:
            print(f'{user.username.title()}')
    print('\n=====\n')


def user_following_ignoring(database_connection, user,
                            index=0, to_list=False):
    """Return list of users being followed or ignored by
    specified user"""
    following_query = userdata.following_iter(database_connection, user)
    ignoring_query = userdata.ignoring_iter(database_connection, user)

    if to_list:
        following_list = [i[index] for i in following_query]
        ignoring_list = [i[index] for i in ignoring_query]
        return following_list, ignoring_list

    following_list = (i[index] for i in following_query)
    ignoring_list = (i[index] for i in ignoring_query)
    return following_list, ignoring_list


def display_users(database_connection, signed_in, page_num):
    """Display users and user relations"""
    (following_list,
     ignoring_list) = user_following_ignoring(database_connection,
                                              signed_in, to_list=True)
    user_list_query = userdata.user_data_iter(database_connection)
    users_page = userinterface.page_number_display('users',
                                                   user_list_query,
                                                   signed_in,
                                                   page_num)
    if not users_page:
        display_no_users_on_page(page_num)
    else:
        display_users_and_relations(users_page, following_list, ignoring_list)
        # sleep(.5)


def select_user(database_connection, action):
    """Check for valid selected user"""
    print(f'Select the user you would like to '
          f'{action} or un{action}')
    selected_user = input('\t==> ').strip().lower()
    try:
        user = [Box(dict(i)) for i in
                userdata.user_data_iter(database_connection)
                if i[1] == selected_user.lower()][0]
        return user
    except IndexError:
        print('This user does not exist.')
        sleep(1)
        return False


def add_remove_user(user, signed_in, database_connection, action):
    """Add or remove user from follow or ignore list"""
    (following_list,
     ignoring_list) = user_following_ignoring(database_connection,
                                              signed_in)
    if action == 'follow':
        list_, second_list_ = following_list, ignoring_list
    elif action == 'ignore':
        list_, second_list_ = ignoring_list, following_list

    if user.user_id in second_list_:
        print('User cannot be ignored and followed at the same time.\n'
              'Remove this user from one of these lists to continue. ')
    elif user.user_id in list_:
        userdata.remove_from_list(database_connection, user, signed_in, action)
        print(f"=====\nNow un{action[:-1] if action.endswith('e') else action}ing "
              f'{user.username.title()}.')
    else:
        userdata.add_to_list(database_connection, user, signed_in, action)
        print(f"=====\nNow {action[:-1] if action.endswith('e') else action}ing "
              f'{user.username.title()}.')
    sleep(1)


def follow_or_ignore(database_connection, signed_in, action):
    """Follow or ignor user."""
    user = select_user(database_connection, action)
    if user:
        add_remove_user(user, signed_in, database_connection, action)


def prompt_for_user_profile(database_connection, signed_in):
    """Return a profile for any user"""
    while True:
        user_row = userdata.get_user_data(database_connection)
        try:
            user = [Box(dict(x)) for x in user_row][0]
        except IndexError:
            print('Something went wrong. Maybe this user does not exist?')
            continue
        (following_list_usernames,
         ignoring_list_usernames) = user_following_ignoring(
             database_connection,
             signed_in,
             index=1,
             to_list=True)

        return user, following_list_usernames, ignoring_list_usernames


def display_profile_following_list(user_following):
    """Display users following list"""
    print('Following: ')
    if user_following:
        for followed_user in user_following:
            print(f'\t{followed_user.title()}')
    else:
        print('\tNot following any users.')


def display_profile_ignoring_list(user_ignoring):
    """Display users ignoring list"""
    print('Ignoring: ')
    if user_ignoring:
        for followed_user in user_ignoring:
            print(f'\t{followed_user.title()}')
    else:
        print('\tNot ignoring any users')


def display_if_following_or_ignoring_profile(user, following_list,
                                             ignoring_list):
    """Display users following or ignoring status"""
    if user.user_id in following_list:
        print(f'Username: {user.username.title()} - Following')
    elif user.user_id in ignoring_list:
        print(f'Username: {user.username.title()} - Ignoring')
    else:
        print(f'Username: {user.username.title()}')


def displey_user_profile(database_connection, signed_in, user,
                         user_following, user_ignoring):
    """Display user profile"""
    (following_list,
     ignoring_list) = user_following_ignoring(database_connection,
                                              signed_in, to_list=True)
    print('\n=====\n')
    display_if_following_or_ignoring_profile(user, following_list, ignoring_list)
    print(f'Location: {user.location}\n')
    # print(f'Bio: {user.biography}')
    display_profile_following_list(user_following)
    display_profile_ignoring_list(user_ignoring)
    print('\n=====\n')


def prompt_for_profile_action(database_connection, user, signed_in):
    """Return a profile for any user"""
    print('> (P) View this users posts')
    print('> (F) Follow or unfollow this user')
    print('> (I) Ignore or unignore this user')
    print('> (B) Back')
    action = input('==> ').strip().upper()
    if action == 'B':
        return 'BREAK' # Break the loop from the user_profile function
    if action == 'P':
        posts = userdata.raw_users_posts(database_connection, user)
        userinterface.display_posts(posts, database_connection,
                                    signed_in, page_num=1)
        sleep(1)
    elif action == 'F':
        add_remove_user(user, signed_in, database_connection, 'follow')
    elif action == 'I':
        add_remove_user(user, signed_in, database_connection, 'ignore')
    else:
        print('Please select a valid option')


def user_profile(con, signed_in):
    """Display individual user profile"""
    (user,
     user_following,
     user_ignoring) = prompt_for_user_profile(con, signed_in)
    while True:
        displey_user_profile(con, signed_in, user, user_following, user_ignoring)
        if prompt_for_profile_action(con, user, signed_in) == 'BREAK':
            break


def user_page_action(action, database_connection, signed_in):
    """Accept action from user page"""
    if action == 'B':
        return 'BREAK'
    if action.isdigit():
        # Test this without this weird logic
        action = int(action)
        if action:
            display_users(database_connection, signed_in, action)
        else:
            print('-' * 50)
            print('No users on page 0. Please go to page 1.')
            print('-' * 50)
    elif action == 'P':
        user_profile(database_connection, signed_in)
        display_users(database_connection, signed_in, 1)
    elif action == 'F':
        follow_or_ignore(database_connection, signed_in, 'follow')
        display_users(database_connection, signed_in, 1)
    elif action == 'I':
        follow_or_ignore(database_connection, signed_in, 'ignore')
        display_users(database_connection, signed_in, 1)
    else:
        print('Please enter a valid option')


def users_main_page(database_connection, signed_in):
    """users page to view and interact with other users"""
    display_users(database_connection, signed_in, 1)
    while True:
        print('> (#) Users page')
        print('> (P) View users profile')
        print('> (F) Follow or unfollow user')
        print('> (I) Ignore or unignore user')
        print('> (B) Back')
        print('Select an action')
        action = input('\t==> ').strip().upper()

        if user_page_action(action, database_connection, signed_in) == 'BREAK':
            break
