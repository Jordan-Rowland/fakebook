"""
This module holds common functions used in other modules. This
module is so separate page modules do not import eachother for
functions.
"""

import itertools

from box import Box

import userdata


def ask_for(message):
    """Basic function to ask the user for some input"""
    print(f'{message}')
    user_input = input('\t==> ').strip()
    return user_input


def validate_posts(database_connection, signed_in):
    """Only show posts from unignored users"""
    cursor = database_connection.cursor()
    validated_posts = cursor.execute('''SELECT p.user_id, p.post_id,
                         username, text, timestamp
                         FROM posts p
                         INNER JOIN users u on u.user_id = p.user_id
                         WHERE p.user_id NOT IN
                                (
                                    SELECT ignored_id FROM ignoring
                                    WHERE ignoring_id = ?
                                )
                         ORDER BY p.post_id desc''', (signed_in.user_id, ))
    return validated_posts


def page_number_display(posts_or_users, raw_data, signed_in, page_num):
    """Calculate how many users or posts are displayed per page"""
    if page_num > 0:
        if posts_or_users == 'posts':
            start_post = signed_in.posts_per_page * (page_num - 1)
            end_post = signed_in.posts_per_page * page_num
            query_gen = (row for row in raw_data)
            results_slice = itertools.islice(query_gen, start_post, end_post)
            results_page = list(results_slice)
            return results_page

        if posts_or_users == 'users':
            start = 15 * (page_num - 1)
            end = 15 * page_num
            user_list_gen = (row for row in raw_data)
            results_slice = itertools.islice(user_list_gen, start, end)
            results = list(results_slice)
            return results


def display_posts(validated_posts, database_connection,
                  signed_in, page_num, post_id_show=False):
    """Display posts in a pretty format. Posts are based on page number
    and and number of posts per page in user timeline. This function
    uses a generator and islice from itertools to return a slice of
    posts per page.
    """
    following_query = userdata.following_iter(database_connection, signed_in)
    following_list = [i[0] for i in following_query]
    results_page = page_number_display('posts',
                                       validated_posts,
                                       signed_in,
                                       page_num)
    if not results_page:
        print('-' * 100)
        print(f'No posts on page {page_num}. Please go back a page.')
        print('-' * 100)
    else:
        print('-' * 100)
        for row in results_page:
            post = Box(dict(row))
            if post.user_id in following_list:
                print(f'|\n|*{post.username.title()}\n|\t\t{post.text}\n|')
            else:
                print(f'|\n|{post.username.title()}\n|\t\t{post.text}\n|')

            if post_id_show:
                print(f'|Post ID: {post.post_id}')
            print(f'|\n|\t\t\t\t\t\t\t\t\t\t{post.timestamp[:10]}')
            print('-' * 100)
