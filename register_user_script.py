from commands.user_commands import register_user

def main():
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    result = register_user(username, email, password)
    print(result)

if __name__ == "__main__":
    main()
