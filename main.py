'''Main page, always run this'''

import userdata
import userinterface

# If having trouble saving items, add users to account???


def main():
    '''Main function'''
    users, posts = userdata.init()
    # initializing = True
    # while initializing:
    #     try:
    #         action = input('Press 1 to create a new account or 2 to '
    #                        'sign into an existing account... > ')
    #         if int(action) == 1:
    #             signed_in = create_account(users)
    #             if signed_in:
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
    userinterface.timeline(users, posts, signed_in, 1)

    while True:
        # Timeline, add page view
        action = userinterface.prompt_for_action()

        if action == 'SIGN OUT':
            userdata.save_users(users)
            userdata.save_posts(posts)
            break

        elif action == 'TIMELINE':
            userinterface.timeline(users, posts, signed_in, 1)

        elif action.isdigit():
            action = int(action)
            userinterface.timeline(users, posts, signed_in, action)

        elif action == 'ACCOUNT SETTINGS':
            userinterface.account(signed_in, posts)
            userinterface.timeline(users, posts, signed_in, 1)

        elif action == 'USERS':
            userinterface.users_page(users, signed_in)
            userinterface.timeline(users, posts, signed_in, 1)

        elif action == 'POST':
            post = input('Type your post:\n\t>')
            posts.append(userinterface.add_post(post, posts, signed_in))
            userinterface.timeline(users, posts, signed_in, 1)


if __name__ == '__main__':
    main()
