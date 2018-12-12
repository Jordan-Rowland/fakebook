import userdata
import userinterface


def main():
    users, posts = userdata.init()
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
        # print(posts)
        print('> T. Timeline')
        print('> A. Account')
        print('> P. Post')
        print('> U. Users')
        print('> O. Sign Out')
        action = input('Select an action\n\t>>>')
        # action = action.upper()


        if action.upper() == 'T':
            userinterface.timeline(posts)
            # pass
        elif action.upper() == 'A': pass
        elif action.upper() == 'P':
            post = input('Type your post:\n\t>')
            posts.append(userinterface.add_post(post))
            userinterface.timeline(posts)
        elif action.upper() == 'U': pass
        elif action.upper() == 'O': 
            userdata._save_posts(users)
            userdata._save_posts(posts)
            break
        

if __name__ == '__main__':
    main()
