from time import sleep
import itertools

from box import Box

import timeline
import userdata

# def display_users(users_, following, ignoring):
#     """Display users and user relations"""
#     print('\n=====\n')
#     for user in users_:
#         if user.user_id in following:
#             print(f'{user.username.title()} (following)')
#         elif user.user_id in ignoring:
#             print(f'{user.username.title()} (ignoring)')
#         else:
#             print(f'{user.username.title()}')
#     print('\n=====\n')
#     sleep(.5)


# def validate_user(users_, selected_user):
#     """Check for valid selected user"""
#     if selected_user.lower() in [user.username.lower() for user in users_]:
#         return True
#     print('This user does not exist.')
#     sleep(1)
#     return False


# def select_user(users_, action):
#     prompt_for_user = print(f'Select the user you would like to '
#         f'{action} or un{action}')
#     selected_user = input('\t>>> ').strip().lower()
#     if validate_user(users_, selected_user):
#         user = [user for user in users_ if selected_user == user.username][0]
#         return user
#     return False


# def add_remove_user(user, list_, second_list_, action):
#     """Add or remove user from follow or ignore list"""
#     if user.user_id in second_list_:
#         print('User cannot be ignored and followed at the same time.\n'
#               'Remove this user from one of these lists to continue. ')
#     elif user.user_id in list_:
#         list_.remove(user.user_id)
#         print(f'=====\nNow un{action[:-1] if action.endswith("e") else action}ing '
#               f'{user.username.title()}.')
#     else:
#         list_.append(user.user_id)
#         print(f'=====\nNow {action[:-1] if action.endswith("e") else action}ing '
#               f'{user.username.title()}.')
#     sleep(1)


# def follow_or_ignore(users_, list_, second_list_, action):
#     """Over all meta-function for following, ignoring"""
#     user = select_user(users_, action)
#     if user:
#         add_remove_user(user, list_, second_list_, action)


# #######################################################
# #####       TEST REFACTOR       #####
# #######################################################


# def prompt_for_user_profile(users_):
#     """Return a profile for any user"""
#     print('Enter the username of the user you would like to view')
#     username = input('\t>>> ')
#     if validate_user(users_, username):
#         user = [user for user in users_ if
#                 username.lower() == user.username.lower()][0]
#         user_following = [friend.username for friend in users_
#                           if friend.user_id in user.following]
#         user_ignoring = [friend.username for friend in users_
#                          if friend.user_id in user.ignoring]
#         return user, user_following, user_ignoring


# # in Whie loop
# def displey_user_profile(signed_in, user, user_following, user_ignoring):
#     print('\n=====\n')
#     if user.user_id in signed_in.following:
#         print(f'Username: {user.username.title()} - Following')
#     elif user.user_id in signed_in.ignoring:
#         print(f'Username: {user.username.title()} - Ignoring')
#     else:
#         print(f'Username: {user.username.title()}')

#     print(f'Location: {user.location}\n')
#     print(f'Bio: {user.biography}')
#     print('Following: ')
#     if user_following:
#         for followed_user in user_following:
#             print(f'\t{followed_user.title()}')
#     else:
#         print('\tNot following any users.')
#     print('Ignoring: ')
#     if user_ignoring:
#         for followed_user in user_ignoring:
#             print(f'\t{followed_user.title()}')
#     else:
#         print('\tNot ignoring any users')
#     print('\n=====\n')


# # in Whie loop
# def prompt_for_profile_action(user, posts_, signed_in):
#     """Return a profile for any user"""
#     print('(P) View this users posts')
#     print('(F) Follow or unfollow this user')
#     print('(I) Ignore or unignore this user')
#     print('(B) Back')
#     action = input('>>> ').strip().upper()

#     if action == 'B':
#         return 'BREAK' # Break the loop from the user_profile function

#     if action == 'P':
#         posts_ = [post for post in posts_ if post.user_id == user.user_id]
#         timeline.timeline([user], posts_, signed_in, 1)
#         sleep(1)

#     elif action == 'F':
#         add_remove_user(user, signed_in.following,
#                         signed_in.ignoring, 'follow')

#     elif action == 'I':
#         add_remove_user(user, signed_in.ignoring,
#                         signed_in.following, 'ignore')
#     else:
#         print('Please select a valid option')

# def user_profile(users_, posts_, signed_in):
#     user, user_following, user_ignoring = prompt_for_user_profile(users_)
#     while True:
#         displey_user_profile(signed_in, user, user_following, user_ignoring)
#         if prompt_for_profile_action(user, posts_, signed_in) == 'BREAK':
#             break


# def users_page(users_, posts_, signed_in):
#     """users page"""
#     while True:
#         display_users(users_, signed_in.following, signed_in.ignoring)
#         print('(P) View users profile')
#         print('(F) Follow or unfollow user')
#         print('(I) Ignore or unignore user')
#         print('(B) Back')
#         print('Select an action')
#         action = input('\t>>> ').strip().upper()

#         if action == 'B':
#             break
#         elif action == 'P':
#             user_profile(users_, posts_, signed_in)
#         elif action == 'F':
#             follow_or_ignore(users_, signed_in.following, signed_in.ignoring, 'follow')
#         elif action == 'I':
#             follow_or_ignore(users_, signed_in.ignoring, signed_in.following, 'ignore')
#         else:
#             print('Please enter a valid option')


#######################################################
##### SQL REFACTOR
#######################################################


def display_users(con, signed_in, page_num):
    """Display users and user relations
    """
    following_query = userdata.following_iter(con, signed_in)
    ignoring_query = userdata.ignoring_iter(con, signed_in)
    following_list = [i[0] for i in following_query]
    ignoring_list = [i[0] for i in ignoring_query]

    user_query = userdata.user_iter(con, signed_in)

    if page_num > 0:
        start = 15 * (page_num - 1)
        end = 15 * page_num
        user_query_gen = (row for row in user_query) # Generator out of iterable
        results = itertools.islice(user_query_gen, start, end)
        query = list(results)

    if not query:
        print('\n=====\n')
        print(f'No posts on page {page_num}. Please go back a page.')
        print('\n=====\n')
    else:
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
        # sleep(.5)


def select_user(con, action):
    """Check for valid selected user
    """
    prompt_for_user = print(f'Select the user you would like to '
                            f'{action} or un{action}')
    selected_user = input('\t>>> ').strip().lower()
    user = [Box(dict(i)) for i in userdata.user_iter(con, selected_user)
            if i[1] == selected_user.lower()][0]
    if user:
        return user
    print('This user does not exist.')
    sleep(1)
    return False


### DON'T NEED THIS FUNCTION
# def select_user(con, action):
#     prompt_for_user = print(f'Select the user you would like to '
#         f'{action} or un{action}')
#     selected_user = input('\t>>> ').strip().lower()
#     if validate_user(con, signed_in, selected_user):
#         user = [user for user in users_ if selected_user == user.username][0]
#         return user
#     return False


### Test this with iterators instead of lists
def add_remove_user(user, signed_in, con, action):
    """Add or remove user from follow or ignore list"""
    c = con.cursor()
    following_query = userdata.following_iter(con, signed_in)
    ignoring_query = userdata.ignoring_iter(con, signed_in)
    following_list = (i[0] for i in following_query)
    ignoring_list = (i[0] for i in ignoring_query)

    if action == 'follow':
        list_, second_list_ = following_list, ignoring_list
    elif action == 'ignore':
        list_, second_list_ = ignoring_list, following_list

    if user.user_id in second_list_:
        print('User cannot be ignored and followed at the same time.\n'
              'Remove this user from one of these lists to continue. ')
    elif user.user_id in list_:
        userdata.remove_from_list(con, user, signed_in, action)
        print(f'=====\nNow un{action[:-1] if action.endswith("e") else action}ing '
              f'{user.username.title()}.')
    else:
        userdata.add_to_list(con, user, signed_in, action)
        print(f'=====\nNow {action[:-1] if action.endswith("e") else action}ing '
              f'{user.username.title()}.')
    sleep(1)


def follow_or_ignore(con, signed_in, action):
    """Function for following or ignoring user
    """
    user = select_user(con, action)
    if user:
        add_remove_user(user, signed_in, con, action)


def prompt_for_user_profile(con):
    """Return a profile for any user"""
    print('Enter the username of the user you would like to view')
    username = input('\t>>> ')
    c = con.cursor()
    query = c.execute('''SELECT * FROM users
                         WHERE username = ?''', (username, ))

    user = [Box(dict(x)) for x in query][0]
    if user:
        following_query = userdata.following_iter(con, user)
        ignoring_query = userdata.ignoring_iter(con, user)
        following_list = [i[0] for i in following_query]
        ignoring_list = [i[0] for i in ignoring_query]
    return user, following_list, ignoring_list


# USER ITERATORS INSTEAD
def displey_user_profile(con, signed_in, user, user_following, user_ignoring):
    """Display user profile"""
    c = con.cursor()
    following_query = userdata.following_iter(con, signed_in)
    ignoring_query = userdata.ignoring_iter(con, signed_in)
    following_list = (i[0] for i in following_query)
    ignoring_list = (i[0] for i in ignoring_query)

    print('\n=====\n')
    if user.user_id in following_list:
        print(f'Username: {user.username.title()} - Following')
    elif user.user_id in ignoring_list:
        print(f'Username: {user.username.title()} - Ignoring')
    else:
        print(f'Username: {user.username.title()}')

    print(f'Location: {user.location}\n')
    # print(f'Bio: {user.biography}')

    print('Following: ')
    if user_following:
        for followed_user in user_following:
            print(f'\t{followed_user.title()}')
    else:
        print('\tNot following any users.')

    print('Ignoring: ')
    if user_ignoring:
        for followed_user in user_ignoring:
            print(f'\t{followed_user.title()}')
    else:
        print('\tNot ignoring any users')

    print('\n=====\n')


# in Whie loop
def prompt_for_profile_action(con, user, user_following,
                              user_ignoring, signed_in):
    """Return a profile for any user"""
    print('(P) View this users posts')
    print('(F) Follow or unfollow this user')
    print('(I) Ignore or unignore this user')
    print('(B) Back')
    action = input('>>> ').strip().upper()

    if action == 'B':
        return 'BREAK' # Break the loop from the user_profile function

    if action == 'P':
        posts_ = [post for post in posts_ if post.user_id == user.user_id]
        timeline.timeline(con, [user], 1)
        sleep(1)

    elif action == 'F':
        add_remove_user(user, signed_in, con, 'follow')
    elif action == 'I':
        add_remove_user(user, signed_in, con, 'ignore')
    else:
        print('Please select a valid option')


def user_profile(con, signed_in):
    user, user_following, user_ignoring = prompt_for_user_profile(con)
    while True:
        displey_user_profile(con, signed_in, user, user_following, user_ignoring)
        if prompt_for_profile_action(con, user, user_following,
                                     user_ignoring, signed_in) == 'BREAK':
            break


def users_page(con, signed_in):
    """users page"""
    display_users(con, signed_in, 1)
    while True:
        print('(P) View users profile')
        print('(F) Follow or unfollow user')
        print('(I) Ignore or unignore user')
        print('(B) Back')
        print('Select an action')
        action = input('\t>>> ').strip().upper()

        if action == 'B':
            break

        elif action.isdigit():
            action = int(action)
            if action:
                display_users(con, signed_in, action)
            else:
                print('-' * 50)
                print('No users on page 0. Please go to page 1.')
                print('-' * 50)

        elif action == 'P':
            user_profile(con, signed_in)
            display_users(con, signed_in, 1)
        elif action == 'F':
            follow_or_ignore(con, signed_in, 'follow')
            display_users(con, signed_in, 1)
        elif action == 'I':
            follow_or_ignore(con, signed_in, 'ignore')
            display_users(con, signed_in, 1)
        else:
            print('Please enter a valid option')
