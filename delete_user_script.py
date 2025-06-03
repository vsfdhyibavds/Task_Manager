from commands.user_commands import delete_user

def main():
    user_id = int(input("Enter user ID to delete: "))
    result = delete_user(user_id)
    print(result)

if __name__ == "__main__":
    main()
