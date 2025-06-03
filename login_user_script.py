from commands.user_commands import login_user

def main():
    username = "new_user"
    password = "password123"
    result = login_user(username, password)
    print(result)

if __name__ == "__main__":
    main()
