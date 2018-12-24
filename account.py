"""Module to handle everything related to user account"""

from time import sleep

from box import Box

import timeline

###### REMOVE USERNAME AND PASSWORD ARGUMENTS WHEN DONE TESTING
def sign_in(username, password, con):
    """Sign in from existing user account"""
    # username = input('Please enter your username:\n>\t')
    # password = input('Please enter your password:\n>\t')

    c = con.cursor()
    query = c.execute('''SELECT * FROM users
                            WHERE username = ?
                            AND password = ?''',
                      (username.lower(), password))

    for row in query:
        signed_in = Box(dict(row))
        print(f"\nSigned in as: {signed_in.username.title()}\n")
        c.close()
        return signed_in
    print('Please sign in as a valid user or create a new account!')
    return False


def new_password_username(parameter, con, signed_in):
    """Update username or password for signed in user
    """
    c = con.cursor()
    print(signed_in[parameter])
    new_parameter = input(f'Type a new {parameter}\n\t>>> ')
    if parameter == 'username':
        query = c.execute(f'SELECT username FROM users WHERE user_id = ?;',
                          (signed_in.user_id,))
    else:
        query = c.execute(f'SELECT password FROM users WHERE user_id = ?;',
                          (signed_in.user_id,))

    query = query.fetchone()
    if signed_in[parameter] == list(query)[0]:
        signed_in[parameter] = new_parameter
    if parameter == 'username':
        c.execute('''UPDATE users
                     SET username = ?
                     WHERE user_id = ?;''',
                  (new_parameter.lower(), signed_in.user_id, ))
    else:
        c.execute('''UPDATE users
                     SET password = ?
                     WHERE user_id = ?;''',
                  (new_parameter.lower(), signed_in.user_id, ))

    print(f'{parameter.title()} Changed!')
    con.commit()
    c.close()
    sleep(1)


def update_timeline_view(con, signed_in):
    """Update posts per page on timeline"""
    print(f'Currently viewing {signed_in.posts_per_page} post(s) per page.')
    sleep(1)
    print("Enter the amount of posts you'd like to see on your "
          "timeline(Please enter a positive integer value).")
    new_posts_per_page = input('\n>>> ').strip()

    c = con.cursor()
    if new_posts_per_page.isdigit():
        c.execute('''UPDATE users
                     SET posts_per_page = ?
                     WHERE user_id = ?;''',
                  (new_posts_per_page, signed_in.user_id))

        signed_in.posts_per_page = int(new_posts_per_page)
        print(f'Currently viewing {signed_in.posts_per_page}'
              f' post(s) per page.')

        sleep(1)
    else:
        print('\nYou must enter a number.\n')
        sleep(1)
    con.commit()
    c.close()


def account(signed_in, con):
    """Account page loop"""
    while True:
        print(f'Username: {signed_in.username} - {signed_in.location}')
        print('(U) Change Username')
        print('(P) Change Password')
        print('(T) Timeline Post Count')
        print('(M) My Recent Posts')
        print('(B) Back')
        action = input('Select an action\n\t>>> ').strip().upper()

        if action == 'P':
            new_password_username('password', con, signed_in)
        elif action == 'U':
            new_password_username('username', con, signed_in)
        elif action == 'T':
            update_timeline_view(con, signed_in)

        elif action == 'M':
            c = con.cursor()
            query = c.execute('''SELECT p.user_id, username, text, timestamp
                                 FROM posts p
                                 INNER JOIN users u on u.user_id = p.user_id
                                 WHERE p.user_id = ?
                                 ORDER BY p.post_id desc''',
                              (signed_in.user_id, ))

            timeline.display_posts(query, con, signed_in, 1)

        elif action == 'B':
            break
