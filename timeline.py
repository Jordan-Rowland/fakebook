from math import floor

from box import Box


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


def validate_posts(posts_, users_, signed_in):
    '''Only show posts from unignored users'''
    validated_posts = []
    for post in reversed(sorted(posts_, key=lambda k: k['post_id'])):
        if post.user_id in signed_in.ignoring:
            continue
        for user in users_:
            if post.user_id == user.user_id:
                if user.user_id in signed_in.following:
                    username = f"*{user.username.title()}"
                    break
                elif post.user_id == user.user_id:
                    username = user.username.title()
                    break
        validated_posts.append(Box({'username': username,
                           'text': post.text,
                           'post_id': post.user_id,
                           'timestamp': post.timestamp
                           }))
    return validated_posts


def display_posts(posts_, signed_in, page_num):
    '''How posts are displayed in timeline'''
    start_post = signed_in.posts_in_timeline * (page_num - 1)
    end_post = signed_in.posts_in_timeline * page_num
    posts_ = posts_[start_post:end_post]
    if not posts_:
        print('-' * 50)
        print(f'No posts on page {page_num}. Please go back a page.')
        print('-' * 50)
    else:
        print('-' * 50)
        for post in posts_:
            print(f"|\n|{post.username}\n|\t\t{post.text}\n|")
            print(f"|\n|\t\t\t\t\t{post.timestamp[:10]}")
            print('-' * 50)


def timeline(users_, posts_, signed_in, page_num):
    '''Display timeline'''
    max_page = floor(len(posts_) / signed_in.posts_in_timeline)
    if page_num <= max_page:
        print(f'\nTimeline: page {page_num} of '
              f'{max_page}\n')
    posts_ = validate_posts(posts_, users_, signed_in)
    display_posts(posts_, signed_in, page_num)

### ADD POST
def add_post(text, posts_, signed_in):
    '''Add new post'''
    _max_post_id = max([post.post_id for post in posts_])
    new_post = {'post_id': _max_post_id + 1,
                'text': text,
                'user_id': signed_in.user_id,
                'timestamp': '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now())}
    return Box(new_post)
