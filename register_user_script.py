from commands.user_commands import register_user

def main():
    username = "new_user"
    email = "new_user@example.com"
    password = "password123"
    result = register_user(username, email, password)
    print(result)

if __name__ == "__main__":
    main()
