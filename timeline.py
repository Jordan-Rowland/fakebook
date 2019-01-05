'''Module to handle all details related to Timeline view'''

import itertools
# from math import floor

from box import Box

import userdata

### TIMELINE
def prompt_for_action():
    '''Prompt for action, main loop for program'''
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


def validate_posts(con, signed_in):
    '''Only show posts from unignored users'''
    c = con.cursor()
    query = c.execute('''SELECT p.user_id, p.post_id,
                         username, text, timestamp
                         FROM posts p
                         INNER JOIN users u on u.user_id = p.user_id
                         WHERE p.user_id NOT IN
                                (
                                    SELECT ignored_id FROM ignoring
                                    WHERE ignoring_id = ?
                                )
                         ORDER BY p.post_id desc''', (signed_in.user_id, ))
    # c.close()
    return query


def display_posts(query, con, signed_in, page_num, post_id_show=False):
    '''Display posts in a pretty format. Posts are based on page number
    and and number of posts per page in user timeline. This function
    uses a generator and islice from itertools to return a slice of
    posts per page.
    '''
    c = con.cursor()

    following_query = userdata.following_iter(con, signed_in)
    following_list = [i[0] for i in following_query]

    if page_num > 0:
        start_post = signed_in.posts_per_page * (page_num - 1)
        end_post = signed_in.posts_per_page * page_num
        query_gen = (row for row in query) # Generator out of iterable
        results = itertools.islice(query_gen, start_post, end_post)
        query = list(results)

    if not query:
        print('-' * 100)
        print(f'No posts on page {page_num}. Please go back a page.')
        print('-' * 100)
    else:
        print('-' * 100)
        for row in query:
            post = Box(dict(row))
            if post.user_id in following_list:
                print(f'|\n|*{post.username.title()}\n|\t\t{post.text}\n|')
            else:
                print(f'|\n|{post.username.title()}\n|\t\t{post.text}\n|')

            if post_id_show:
                print(f'|Post ID: {post.post_id}')
            print(f'|\n|\t\t\t\t\t\t\t\t\t\t{post.timestamp[:10]}')
            print('-' * 100)
    c.close()


def timeline(con, signed_in, page_num):
    '''Display timeline. This function used to return the page number
    of the timeline out of macimum page, but it's a bit trickier to
    work out with query iterators instead of JSON.
    '''
            # max_page = floor(len(posts_) / signed_in.posts_in_timeline)
            # if page_num <= max_page:
    print(f'\nTimeline: page {page_num}')
    query = validate_posts(con, signed_in)
    display_posts(query, con, signed_in, page_num)
