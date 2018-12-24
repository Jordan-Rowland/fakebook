"""Main page, always run this"""

import userdata
import usersmodule
import account
import timeline


def main():
    """Main function that runs the loop state for entire program"""
    con = userdata.init()

    # initializing = True
    # while initializing:
    #     try:
    #         action = input('Press 1 to create a new account or 2 to '
    #                        'sign into an existing account... > ')
    #         if int(action) == 1:
    #             signed_in = account.create_account(users)
    #             if signed_in:
    #                 initializing = False
    #             else:
    #                 continue
    #         elif int(action) == 2:
    #             if account.sign_in(users):
    #                 initializing = False
    #             else:
    #                 continue
    #     except:
    #         print('Not a valid operation')

    signed_in = account.sign_in('jordan00', 'jr11', con)
    timeline.timeline(con, signed_in, 1)

    while True:
        action = timeline.prompt_for_action()
        if action == 'SIGN OUT':
            con.close()
            break
        elif action.isdigit():
            action = int(action)
            if action:
                timeline.timeline(con, signed_in, action)
            else:
                print('-' * 50)
                print('No posts on page 0. Please go to page 1.')
                print('-' * 50)

        elif action == 'ACCOUNT SETTINGS':
            account.account(signed_in, con)
            timeline.timeline(con, signed_in, 1)
        elif action == 'USERS':
            usersmodule.users_page(con, signed_in)
            timeline.timeline(con, signed_in, 1)
        elif action == 'POST':
            post = input('Type your post:\n\t>')
            userdata.add_post(con, post, signed_in)
            timeline.timeline(con, signed_in, 1)


if __name__ == '__main__':
    main()
