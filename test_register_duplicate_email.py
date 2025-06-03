from commands.user_commands import register_user

def test_duplicate_email():
    # Register first user
    result1 = register_user("user1", "duplicate@example.com", "password1")
    print("First registration:", result1)

    # Attempt to register second user with same email
    result2 = register_user("user2", "duplicate@example.com", "password2")
    print("Second registration (should fail):", result2)

if __name__ == "__main__":
    test_duplicate_email()
