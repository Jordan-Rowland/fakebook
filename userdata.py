"""
All data logic is here. INitialize database, add posts, and return
user lists.
"""

import datetime
import sqlite3

from box import Box

import userinterface


def init():
    """Initiate posts and users"""

    database_connection = sqlite3.connect('fakebook/fk.db')
    database_connection.row_factory = sqlite3.Row
    return database_connection


def following_iter(database_connection, signed_in):
    """Returns the signed in user's following list as an iterator"""
    cursor = database_connection.cursor()
    following_query = cursor.execute('''SELECT followed_id, username
                                        FROM following f
                                        INNER JOIN users u on u.user_id = f.followed_id
                                        WHERE following_id = ?''',
                                     (signed_in.user_id, ))
    return following_query


def ignoring_iter(database_connection, signed_in):
    """Returns the signed in user's ignoring list as an iterator"""
    cursor = database_connection.cursor()
    ignoring_query = cursor.execute('''SELECT ignored_id, username
                                       FROM ignoring i
                                       INNER JOIN users u on u.user_id = i.ignored_id
                                       WHERE ignoring_id = ?''',
                                    (signed_in.user_id, ))
    return ignoring_query


def user_data_iter(database_connection):
    """Returns the signed in user's ignoring list as an iterator"""
    cursor = database_connection.cursor()
    users_query = cursor.execute('''SELECT * FROM users;''')
    return users_query


def add_post(database_connection, post, signed_in):
    """Add new post to timeline."""
    cursor = database_connection.cursor()
    cursor.execute('SELECT MAX(post_id) FROM posts;')
    max_post_id = Box(dict(cursor.fetchone())).values()[0]
    cursor.execute('''INSERT INTO posts VALUES (?, ?, ?, ?);''',
                   ((max_post_id + 1), post,
                    '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()),
                    signed_in.user_id,))
    database_connection.commit()
    cursor.close()


def remove_post(database_connection, signed_in, input_post_id):
    """Delete own post from database"""
    cursor = database_connection.cursor()
    cursor.execute('''DELETE FROM posts
                      WHERE user_id = ?
                      AND post_id = ?''',
                   (signed_in.user_id, input_post_id, ))

    database_connection.commit()
    cursor.close()


def add_to_list(database_connection, user, signed_in, action):
    """Add user to following or ignoring list of signed in users"""
    cursor = database_connection.cursor()
    query = cursor.execute('''SELECT max(f_id), max(i_id)
                              FROM following
                              INNER JOIN ignoring;''')

    max_ids = [i for i in query][0]
    new_f_id = max_ids[0] + 1
    new_i_id = max_ids[1] + 1

    if action == 'follow':
        cursor.execute('''INSERT INTO following VALUES (?, ?, ?);''',
                       (new_f_id, signed_in.user_id,
                        user.user_id, ))
    elif action == 'ignore':
        cursor.execute('''INSERT INTO ignoring VALUES (?, ?, ?);''',
                       (new_i_id, signed_in.user_id,
                        user.user_id, ))
    database_connection.commit()
    cursor.close()


def remove_from_list(database_connection, user, signed_in, action):
    """Remove user to following or ignoring list of signed in users"""
    cursor = database_connection.cursor()

    if action == 'follow':
        cursor.execute('''DELETE FROM following
                          WHERE following_id = ?
                          AND followed_id = ?;''',
                       (signed_in.user_id, user.user_id, ))

    elif action == 'ignore':
        cursor.execute('''DELETE FROM ignoring
                          WHERE ignoring_id = ?
                          AND ignored_id = ?;''',
                       (signed_in.user_id, user.user_id, ))

    database_connection.commit()
    cursor.close()


def insert_new_user(database_connection, user_data):
    """Insert new user to database"""
    cursor = database_connection.cursor()
    cursor.execute('INSERT INTO users VALUES (?,?,?,?,?)', user_data)
    database_connection.commit()
    cursor.close()
    return True


def set_new_username(database_connection, signed_in, new_username, ):
    """Insert new username for signed in user to database"""
    cursor = database_connection.cursor()
    cursor.execute('''UPDATE users
                      SET username = ?
                      WHERE user_id = ?;''',
                   (new_username.lower(), signed_in.user_id, ))
    database_connection.commit()
    cursor.close()


def set_new_password(database_connection, signed_in, new_password, ):
    """Insert new password for signed in user to database"""
    cursor = database_connection.cursor()
    cursor.execute('''UPDATE users
                      SET password = ?
                      WHERE user_id = ?;''',
                   (new_password, signed_in.user_id, ))
    database_connection.commit()
    cursor.close()


def return_self_posts(database_connection, signed_in):
    """Return signed in users posts"""
    cursor = database_connection.cursor()
    query = cursor.execute('''SELECT p.user_id, post_id,
                              username, text, timestamp
                              FROM posts p
                              INNER JOIN users u on
                                  u.user_id = p.user_id
                              WHERE p.user_id = ?
                              ORDER BY p.post_id desc''',
                           (signed_in.user_id, ))
    return query


def get_user_data(database_connection):
    """Return user data for profile view"""
    username = userinterface.ask_for('Enter the user you would like to view')
    cursor = database_connection.cursor()
    user_row = cursor.execute('''SELECT * FROM users
                                 WHERE username = ?''', (username, ))

    return user_row


def raw_users_posts(database_connection, user):
    """Pull users posts to display"""
    cursor = database_connection.cursor()
    posts = cursor.execute('''SELECT p.user_id, username, text, timestamp
                              FROM posts p
                              INNER JOIN users u on u.user_id = p.user_id
                              WHERE p.user_id = ?
                              ORDER BY p.post_id desc''', (user.user_id, ))
    return posts
