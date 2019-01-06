"""Module to handle all details related to Timeline view"""

# from math import floor

import userinterface


def prompt_for_timeline_action():
    """Prompt for action, main loop for program"""
    while True:
        print('\n=====\n')
        print('> (#) Timeline Page')
        print('> (A) Account')
        print('> (U) Users')
        print('> (P) Post')
        print('> (O) Sign Out')
        action = input('\nSelect an action\n\t==> ').strip().upper()

        options = {'A': 'ACCOUNT SETTINGS',
                   'U': 'USERS',
                   'P': 'POST',
                   'O': 'SIGN OUT'}

        if action.isdigit():
            return action
        if action in options.keys():
            return options[action]
        continue


def timeline(database_connection, signed_in, page_num):
    """Display timeline. This function used to return the page number
    of the timeline out of maximum page, but it's a bit trickier to
    work out with query iterators instead of JSON.
    """
            # max_page = floor(len(posts_) / signed_in.posts_in_timeline)
            # if page_num <= max_page:
    print(f'\nTimeline: page {page_num}')
    validated_posts = userinterface.validate_posts(database_connection,
                                                   signed_in)
    userinterface.display_posts(validated_posts,
                                database_connection,
                                signed_in, page_num)
