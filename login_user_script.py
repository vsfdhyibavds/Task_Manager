from commands.user_commands import login_user

def main():
    username = input("Enter username: ")
    password = input("Enter password: ")
    result = login_user(username, password)
    print(result)

if __name__ == "__main__":
    main()
