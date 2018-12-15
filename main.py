'''Main page, always run this'''

import userdata
import userinterface

# If having trouble saving items, add users to account???

def main():
    '''Main function'''
    userdata.init()
    posts = userdata.posts()
    users = userdata.users()
    # initializing = True
    # while initializing:
    #     try:
    #         action = input('Press 1 to create a new account or 2 to \
    #                         sign into an existing account...')
    #         if int(action) == 1:
    #             if create_account(users):
    #                 initializing = False
    #             else:
    #                 continue
    #         elif int(action) == 2:
    #             if sign_in(users):
    #                 initializing = False
    #             else:
    #                 continue
    #     except:
    #         print('Not a valid operation')
    signed_in = userinterface.sign_in('Jordan00', 'jr11', users)

    while True:
        action = userinterface.prompt_for_action()

        if action == 'SIGN OUT':
            userdata._save_users(users)
            userdata._save_posts(posts)
            break

        elif action == 'TIMELINE':
            userinterface.timeline(posts) # PAGE NUMBER

        elif action == 'ACCOUNT':
            userinterface.account(signed_in)

        elif action == 'USERS':
            userinterface.users(users)

        elif action == 'POST':
            post = input('Type your post:\n\t>')
            posts.append(userinterface.add_post(post))
            userinterface.timeline(posts)


if __name__ == '__main__':
    main()
