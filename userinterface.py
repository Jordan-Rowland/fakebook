from datetime import datetime
import userdata 


def add_post(text):
    global signed_in
    signed_in = userdata.signed_in
    post_ids = []
    for post in userdata.posts:
        post_ids.append(int(post['post_id']))
    new_post = {'post_id': str(max(post_ids) + 1), 'text': text, 'user_id': signed_in['user_id'],'timestamp': '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now())}
    userdata.posts.append(new_post)
    userdata._save_posts()


def follow_ignore(username,follow_or_ignore):
    user_id = False
    for user in userdata.users:
        if username.lower() == user['username']:
            user_id = user['user_id']
    if user_id:
        if follow_or_ignore == 'follow':
            try:
                userdata.signed_in['following'].append(user_id)
            except:
                print('something wen\'t wrong, user not in list.')
        
        elif follow_or_ignore == 'ignore':
            try:
                userdata.signed_in['ignoring'].append(user_id)
            except:
                print('something wen\'t wrong, user not in list.')
        
        elif follow_or_ignore == 'unfollow':
            try:
                userdata.signed_in['following'].remove(user_id)
            except:
                print('something wen\'t wrong, user not in list.')
        
        elif follow_or_ignore == 'unignore':
            try:
                userdata.signed_in['ignoring'].remove(user_id)
                userdata.signed_in
            except:
                print('something wen\'t wrong, user not in list.')
        
        else:
            print('Please select update type')
    else:
        print('operation failed')
