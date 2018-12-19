from time import sleep

import timeline

from box import Box


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
    sleep(.5)


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
        user = [user for user in users_ if
                username.lower() == user.username.lower()][0]
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
def prompt_for_profile_action(user, posts_, signed_in):
    '''Return a profile for any user'''
    print('(P) View this users posts')
    print('(F) Follow or unfollow this user')
    print('(I) Ignore or unignore this user')
    print('(B) Back')
    action = input('>>> ').strip().upper()

    if action == 'B':
        return 'BREAK' # Break the loop from the user_profile function

    if action == 'P':
        posts_ = [post for post in posts_ if post.user_id == user.user_id]
        timeline.timeline([user], posts_, signed_in, 1)
        sleep(1)

    elif action == 'F':
        add_remove_user(user, signed_in.following,
                        signed_in.ignoring, 'follow')

    elif action == 'I':
        add_remove_user(user, signed_in.ignoring,
                        signed_in.following, 'ignore')
    else:
        print('Please select a valid option')

def user_profile(users_, posts_, signed_in):
    user, user_following, user_ignoring = prompt_for_user_profile(users_)
    while True:
        displey_user_profile(signed_in, user, user_following, user_ignoring)
        if prompt_for_profile_action(user, posts_, signed_in) == 'BREAK':
            break


def users_page(users_, posts_, signed_in):
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
            user_profile(users_, posts_, signed_in)
        elif action == 'F':
            follow_or_ignore(users_, signed_in.following, signed_in.ignoring, 'follow')
        elif action == 'I':
            follow_or_ignore(users_, signed_in.ignoring, signed_in.following, 'ignore')
        else:
            print('Please enter a valid option')
