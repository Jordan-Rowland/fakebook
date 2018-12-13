import userdata
import userinterface


def main():
    userdata.init()
    posts = userdata.posts()
    users = userdata.users()
    # initializing = True
    # while initializing:
    #     try:
    #         action = input('Press 1 to create a new account or 2 to \
    #                         sign into an existing account...')
    #         if int(action) == 1:
    #             if create_account():
    #                 initializing = False
    #             else:
    #                 continue
    #         elif int(action) == 2:
    #             if sign_in():
    #                 initializing = False
    #             else:
    #                 continue
    #     except:
    #         print('Not a valid operation')
    signed_in = userinterface.sign_in('jordan','jr11')

    while True:
        # userinterface.timeline(posts)
        action = userinterface.prompt_for_action()

        if action == 'SIGN OUT':
            userdata._save_users(users)
            userdata._save_posts(posts)
            break

        elif action == 'TIMELINE':
            userinterface.timeline(posts)
        
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
