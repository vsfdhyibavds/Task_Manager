from commands.user_commands import update_user

def main():
    user_id = int(input("Enter user ID to update: "))
    updates = {}

    username = input("Enter new username (leave blank to skip): ")
    if username:
        updates["username"] = username

    email = input("Enter new email (leave blank to skip): ")
    if email:
        updates["email"] = email

    password = input("Enter new password (leave blank to skip): ")
    if password:
        updates["password"] = password

    if not updates:
        print("No updates provided.")
        return

    result = update_user(user_id, updates)
    print(result)

if __name__ == "__main__":
    main()
