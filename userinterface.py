from box import Box
from datetime import datetime
# from datetime import datetime
# '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now())
from random import randint as r
import userdata



users, posts = userdata.init()


def create_account():
    global signed_in
    username = input('Please enter a new username:\n>\t')
    password = input('Please enter a new password:\n>\t')
    user_id = f"{username[0]}{username[-1]}{r(1,999)}"
    for user in users:
        if username == user['username']:
            print('Username is already taken.')
            return False
    users.append(Box({'username': username,
                      'password': password,
                      'user_id': user_id,
                      'following': [],
                      'ignoring': []}))
    signed_in = Box({'username': username,
                     'password': password,
                     'user_id': user_id,
                     'following': [],
                     'ignoring': []})
    userdata._save_users()
    # userdata._load_users()
    return signed_in


def sign_in(username,password):
    global signed_in
    # username = input('Please enter your username:\n>\t')
    # password = input('Please enter your password:\n>\t')
    for user in users:
        if username == user.username and password == user.password:
            signed_in = user
            print(f"Signed in as: {signed_in.username.title()}")
            return signed_in
        else:
            print('Please sign in as a valid user or create a new account!')
            return False


# Need to assign username
def validate_posts(posts):
    # print(posts)
    # global _posts
    _posts = []
    for post in posts[::-1]:
        if post.user_id in signed_in.ignoring:
            continue
        for user in users:
            if post['user_id'] == user['user_id']:
                if user['user_id'] in signed_in['following']:
                    username = f"*{user['username'].title()}"
                    break
                elif post['user_id'] == user['user_id']:
                    username = user['username'].title()
                    break
        text = post['text']
        _posts.append(Box({'username': username,
                       'text': text,
                       'post_id': post.user_id,
                       'timestamp': post.timestamp
                       }))
    return _posts


def display_posts(posts):
    # global _posts
    print(posts)
    print('-' * 50)
    for post in posts:
        print(f"|\n|\n|{post.username}\n|\t{post.text}\n|")
        print(f"|\n|\t\t\t\t{post.timestamp[:10]}")
        print('-' * 50)


def timeline(posts):
    print('Timeline:')
    _posts = validate_posts(posts)
    display_posts(_posts)


def add_post(text):
    global signed_in
    post_ids = [int(post.post_id) for post in posts]
    # for post in posts:
        # post_ids.append(int(post['post_id']))
    new_post = {'post_id': str(max(post_ids) + 1),
                'text': text,
                'user_id': signed_in['user_id'],
                'timestamp': '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now())}
    # posts.append(new_post)
    return Box(new_post)
    # userdata._save_posts(new_post)


# def follow_ignore(username,follow_or_ignore):
#     user_id = False
#     for user in users:
#         if username.lower() == user['username']:
#             user_id = user['user_id']
#     if user_id:
#         if follow_or_ignore == 'follow':
#             try:
#                 userdata.signed_in['following'].append(user_id)
#             except:
#                 print('something wen\'t wrong, user not in list.')
        
#         elif follow_or_ignore == 'ignore':
#             try:
#                 userdata.signed_in['ignoring'].append(user_id)
#             except:
#                 print('something wen\'t wrong, user not in list.')
        
#         elif follow_or_ignore == 'unfollow':
#             try:
#                 userdata.signed_in['following'].remove(user_id)
#             except:
#                 print('something wen\'t wrong, user not in list.')
        
#         elif follow_or_ignore == 'unignore':
#             try:
#                 userdata.signed_in['ignoring'].remove(user_id)
#                 userdata.signed_in
#             except:
#                 print('something wen\'t wrong, user not in list.')
        
#         else:
#             print('Please select update type')
#     else:
#         print('operation failed')
