""" All data logic is here """


import json
import os
import sqlite3

from box import Box

import querytools

def init():
    """Initiate posts and users"""
    # _users = _load_users()
    # _posts = _load_posts()
    # _users = [Box(user) for user in _users]
    # _posts = [Box(post) for post in _posts]

    # return _users, _posts
    con = sqlite3.connect('fakebook/fk.db')
    con.row_factory = sqlite3.Row
    return con


def following_iter(con, signed_in):
    """Returns the signed in user's following list as an iterator"""
    c = con.cursor()
    following_query = c.execute('''SELECT followed_id FROM following
                                   WHERE following_id = ?''',
                                   (signed_in.user_id, ))
    return following_query


def ignoring_iter(con, signed_in):
    """Returns the signed in user's ignoring list as an iterator"""
    c = con.cursor()
    ignoring_query = c.execute('''SELECT ignored_id FROM ignoring
                                  WHERE ignoring_id = ?''',
                                  (signed_in.user_id, ))
    return ignoring_query


def user_iter(con, signed_in):
    """Returns the signed in user's ignoring list as an iterator"""
    c = con.cursor()
    users_query = c.execute('''SELECT * FROM users;''')
    return users_query


def add_post(con, post, signed_in):
    """Add new post to timeline."""
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


def add_to_list(con, user, signed_in, action):
    """Add user to following or ignoring list of signed in users"""
    c = con.cursor()
    query = c.execute('''SELECT max(f_id), max(i_id)
                         FROM following
                         INNER JOIN ignoring;''')

    max_ids = [i for i in query][0]
    new_f_id = max_ids[0] + 1
    new_i_id = max_ids[1] + 1

    if action == 'follow':
        c.execute('''INSERT INTO following VALUES
                    (?, ?, ?);''',
                       (new_f_id,
                        signed_in.user_id,
                        user.user_id, ))
    elif action == 'ignore':
        c.execute('''INSERT INTO ignoring VALUES
                    (?, ?, ?);''',
                       (new_i_id,
                        signed_in.user_id,
                        user.user_id, ))
    con.commit()
    c.close()


def remove_from_list(con, user, signed_in, action):
    """Remove user to following or ignoring list of signed in users"""
    c = con.cursor()

    if action == 'follow':
        c.execute('''DELETE FROM following
                     WHERE following_id = ?
                     AND followed_id = ?;''',
                     (signed_in.user_id, user.user_id, ))

    elif action == 'ignore':
        c.execute('''DELETE FROM ignoring
                     WHERE ignoring_id = ?
                     AND ignored_id = ?;''',
                     (signed_in.user_id, user.user_id, ))

    con.commit()
    c.close()

# def _load_posts():
#     """If file exists, read from file. Else, initiate empty list as items"""
#     if os.path.exists('fakebook/posts.json'):
#         with open('fakebook/posts.json', 'r') as file:
#             _posts = json.loads(file.read())
#     else:
#         _posts = []
#     return _posts


# def save_posts(posts):
#     """Save posts list to File"""
#     with open('fakebook/posts.json', 'w') as file:
#         file.write(json.dumps(posts, indent=4, sort_keys=True))


# def _load_users():
#     """If file exists, read from file. Else, initiate empty list as items"""
#     if os.path.exists('fakebook/users.json'):
#         with open('fakebook/users.json', 'r') as file:
#             _users = json.loads(file.read())
#     else:
#         _users = []
#     return _users


# def save_users(users):
#     """Save users list to File"""
#     with open('fakebook/users.json', 'w') as file:
#         file.write(json.dumps(users, indent=4, sort_keys=True))
