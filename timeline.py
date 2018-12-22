# from itertools import islice
from datetime import datetime
from math import floor


from box import Box

import itertools

### TIMELINE
def prompt_for_action():
    """Prompt for action, main loop for program"""
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

#############################################################################
##### Testing SQL reading
#############################################################################

def validate_posts(con, signed_in):
    """Only show posts from unignored users"""
    c = con.cursor()
    query = c.execute('''SELECT username, text, timestamp
                         FROM posts p
                         INNER JOIN users u on u.user_id = p.user_id
                         WHERE p.user_id NOT IN
                            (
                                SELECT ignored_id FROM ignoring
                                WHERE ignoring_id = ?
                            )
                         ORDER BY p.post_id desc''',
                                (signed_in.user_id, ))
    # c.close()
    return query


def display_posts(query, signed_in, page_num):
    """Display posts in a pretty format. Posts are based on page number
    and and number of posts per page in user timeline. This function
    uses a generator and islice from itertools to return a slice of
    posts per page.
    """
    if page_num > 0:
        start_post = signed_in.posts_per_page * (page_num - 1)
        end_post = signed_in.posts_per_page * page_num
        query_gen = (row for row in query) # Generator out of iterable
        results = itertools.islice(query_gen, start_post, end_post)
        query = list(results)

    if not query:
        print('-' * 50)
        print(f'No posts on page {page_num}. Please go back a page.')
        print('-' * 50)
    else:
        print('-' * 50)
        for row in query:
            post = Box(dict(row))
            print(f"|\n|{post.username.title()}\n|\t\t{post.text}\n|")
            print(f"|\n|\t\t\t\t\t{post.timestamp[:10]}")
            print('-' * 50)

#############################################################################
#############################################################################

""" THIS IS THE ORIGINAL CODE"""
# def validate_posts(posts_, users_, signed_in):
#     """Only show posts from unignored users"""
#     validated_posts = []
#     for post in reversed(sorted(posts_, key=lambda k: k['post_id'])):
#         if post.user_id in signed_in.ignoring:
#             continue
#         for user in users_:
#             if post.user_id == user.user_id:
#                 if user.user_id in signed_in.following:
#                     username = f"*{user.username.title()}"
#                     break
#                 elif post.user_id == user.user_id:
#                     username = user.username.title()
#                     break
#         validated_posts.append(Box({'username': username,
#                            'text': post.text,
#                            'post_id': post.user_id,
#                            'timestamp': post.timestamp
#                            }))
#     return validated_posts


# def display_posts(posts_, signed_in, page_num):
#     """How posts are displayed in timeline"""
#     start_post = signed_in.posts_in_timeline * (page_num - 1)
#     end_post = signed_in.posts_in_timeline * page_num
#     posts_ = posts_[start_post:end_post]
#     if not posts_:
#         print('-' * 50)
#         print(f'No posts on page {page_num}. Please go back a page.')
#         print('-' * 50)
#     else:
#         print('-' * 50)
#         for post in posts_:
#             print(f"|\n|{post.username}\n|\t\t{post.text}\n|")
#             print(f"|\n|\t\t\t\t\t{post.timestamp[:10]}")
#             print('-' * 50)
"""END OF ORIGINAL CODE"""

#############################################################################
##### Testing SQL reading
#############################################################################

def timeline(con, signed_in, page_num):
    """Display timeline. This function used to return the page number
    of the timeline out of macimum page, but it's a bit trickier to
    work out with query iterators instead of JSON.
    """
            # max_page = floor(len(posts_) / signed_in.posts_in_timeline)
            # if page_num <= max_page:
    print(f'\nTimeline: page {page_num}')
    query = validate_posts(con, signed_in)
    display_posts(query, signed_in, page_num)


#############################################################################
#############################################################################

"""ORIGINAL CODE"""
# def timeline(users_, posts_, signed_in, page_num):
#     """Display timeline"""
#     max_page = floor(len(posts_) / signed_in.posts_in_timeline)
#     if page_num <= max_page:
#         print(f'\nTimeline: page {page_num} of '
#               f'{max_page}\n')
#     posts_ = validate_posts(posts_, users_, signed_in)
#     display_posts(posts_, signed_in, page_num)
"""END OF ORIGINAL CODE"""

# ### ADD POST
# def add_post(text, posts_, signed_in):
#     """Add new post"""
#     _max_post_id = max([post.post_id for post in posts_])
#     new_post = {'post_id': _max_post_id + 1,
#                 'text': text,
#                 'user_id': signed_in.user_id,
#                 'timestamp': '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now())}

#     return Box(new_post)

###############################################################################
##### Testing SQL
###############################################################################

### ADD POST
def add_post(con, post, signed_in):
    """Add new post to timeline.
    """
    c = con.cursor()
    c.execute('SELECT MAX(post_id) FROM posts;')
    max_post_id = Box(dict(c.fetchone())).values()[0]
    c.execute('''INSERT INTO posts
                    VALUES
                    (?, ?, ?, ?);''',
                    ((max_post_id + 1),
                    post,
                    '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now()),
                    signed_in.user_id,))
    con.commit()
    c.close()

###############################################################################
###############################################################################
