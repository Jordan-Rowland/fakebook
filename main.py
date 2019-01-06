"""Main page, do not import this"""

import userdata
import usersmodule
import account
import timeline


def main():
    """Main function that runs the loop state for entire program"""
    database_connection = userdata.init()

    signed_in = account.sign_in_or_create_user(database_connection)
    # while True:
    #     print('Press (N) to create a new account or (S) to '
    #           'sign into an existing account. Press (X) to exit.')
    #     action = input('\t==> ').strip().upper()
    #     if action == 'N':
    #         signed_in = account.create_account(database_connection)
    #         if signed_in:
    #             break
    #         else:
    #             continue
    #     elif action == 'S':
    #         signed_in = account.sign_in(database_connection)
    #         if signed_in:
    #             break
    #         else:
    #             continue
    #     elif action == 'X':
    #         # print('Bye!')
    #         sys.exit()
    #     print('Not a valid operation')

    # signed_in = account.sign_in('jordan00', 'Jordan!23', database_connection)
    timeline.timeline(database_connection, signed_in, 1)

    while True:
        action = timeline.prompt_for_timeline_action()
        if action == 'SIGN OUT':
            database_connection.close()
            print('Bye!')
            break
        elif action.isdigit():
            action = int(action)
            if action:
                timeline.timeline(database_connection, signed_in, action)
            else:
                print('-' * 50)
                print('No posts on page 0. Please go to page 1.')
                print('-' * 50)

        elif action == 'ACCOUNT SETTINGS':
            account.account(signed_in, database_connection)
            timeline.timeline(database_connection, signed_in, 1)
        elif action == 'USERS':
            usersmodule.users_main_page(database_connection, signed_in)
            timeline.timeline(database_connection, signed_in, 1)
        elif action == 'POST':
            post = input('Type your post:\n\t>')
            userdata.add_post(database_connection, post, signed_in)
            timeline.timeline(database_connection, signed_in, 1)


if __name__ == '__main__':
    main()
