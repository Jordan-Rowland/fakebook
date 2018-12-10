from userdata import *
from userinterface import *

def main():
    init()
    initializing = True
    while initializing:
        try:
            action = input('Press 1 to create a new account or 2 to sign into an existing account...')
            if int(action) == 1:
                if create_account():
                    initializing = False
                else:
                    continue
            elif int(action) == 2:
                if sign_in():
                    initializing = False
                else:
                    continue
        except:
            print('Not a valid operation')
    

    while True:
        print('> 1. Timeline')
        print('> 2. Post')
        print('> 3. Show Users')
        print('> 4. Follow User')
        print('> 5. Unfollow User')
        print('> 6. Ignore User')
        print('> 7. Unignore User')
        print('> 8. Sign Out')
        action = input('Select an action\n\t>>>')
        action = int(action)



        # landing(username.lower(), password.lower(),users)

        if action == 1:
            timeline()
        elif action == 2:
            post = input('Type your post:\n\t>')
            add_post(post)
            timeline()
        elif action == 3:
            for user in userdata.users:
                if user['user_id'] in userdata.signed_in['following']:
                    print(f"{user['username']} - following")
                elif user['user_id'] in userdata.signed_in['ignoring']:
                    print(f"{user['username']} - ignoring")
                else:
                    print(f"{user['username']}")
        elif action == 4:
            user = input('Type the username of the user you would like to follow:\n\t>')
            follow_ignore(user,'follow')
            timeline()
        elif action == 5:
            print('Users you are following:')
            for user in userdata.users:
                if user['user_id'] in userdata.signed_in['following']:
                    print(user['username'])
            user = input('Type the username of the user you would like to unfollow:\n\t>')
            follow_ignore(user,'unfollow')
            timeline()
        elif action == 6:
            user = input('Type the username of the user you would like to ignore:\n\t>')
            follow_ignore(user,'ignore')
            timeline()
        elif action == 7:
            print('Users you are ignoring:')
            for user in userdata.users:
                if user['user_id'] in userdata.signed_in['ignoring']:
                    print(f"{user['username']}")
            user = input('Type the username of the user you would like to unignore:\n\t>')
            follow_ignore(user,'unignore')
            timeline()
        elif action == 8:
            break

if __name__ == '__main__':
    main()