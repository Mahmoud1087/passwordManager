import json
import random
import string
from encryption import *

PASSWORDLENGTH = 16

symbols_pool = list(string.ascii_letters + string.digits + string.punctuation)

# $env:KEY = "################"  <-- Saved in my laptop's environment variables.


def encrypt(data):
    """
    Encrypts the given data using the encryption key.
    """

    encrypted_data = encrypt_data(data)

    return encrypted_data


def decrypt(encrypted_data):
    """
    Decrypts the given encrypted data using the encryption key.
    """

    decrypted_data = decrypt_data(encrypted_data)
    return decrypted_data


def create_user():
    """
    Prompts the user to create a new account by entering a username and password.
    Saves the new user's credentials to the credentials.json file.
    """

    username = input("Enter a new username: ")
    password = input("Enter a new password: ")
    encrypted_password = encrypt(password)
    user_data = {
        "username": username,
        "password": encrypted_password
    }

    try:
        with open("credentials.json", "r") as f:
            credentials = json.load(f)
            if len(credentials) == 0:
                last_id = 1000
            else:
                last_id = max(credentials.keys())

            curr_id = str(int(last_id) + 1)
            user_data = {
                curr_id: user_data
            }
            credentials.update(user_data)

    except FileNotFoundError:
        with open("credentials.json", "w") as f:
            first_user = {'1001': user_data}
            json.dump(first_user, f, indent=4)

    else:
        with open("credentials.json", "w") as f:
            json.dump(credentials, f, indent=4)


def login():
    """
    Prompts the user to enter a password and returns the entered password.
    """

    try:
        with open("credentials.json", "r") as f:
            credentials = json.load(f)
            if len(credentials) == 0:
                return False, -1
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            encrypted_password = encrypt(password)

            for id, _ in credentials.items():
                if credentials[id]['username'] == username and credentials[id]['password'] == encrypted_password:
                    print('Login successful!')
                    return True, id
            print("Login failed!")
            return False, -1

    except FileNotFoundError:
        print("No users found. Please create a new account.")
        return False, -1


def check_account(id, platform):
    """
    Checks if a saved account already exists for the given platform.
    """
    try:
        with open(f"{id}saved_passwords.json", "r") as f:
            saved_passwords = json.load(f)
            for plat, _ in saved_passwords.items():
                if plat == platform:
                    return True

    except FileNotFoundError:
        print("There are no saved accounts yet.")
        return False

    print(f"There is no saved accounts for {platform}.")
    return False


def generate_password(platform, password=""):
    """
    Generates a random password.
    """
    if len(password) > 0:
        pass
    else:
        password = ""

        for _ in range(PASSWORDLENGTH):
            password += random.choice(symbols_pool)

    use_generated_password = (input(f"Recommended password for {platform}: {password} [y/n]? ")).lower()

    if use_generated_password == 'y':
        return password
    elif use_generated_password == 'n':
        return input("Enter a new password: ")
    else:
        print("Please enter 'y' or 'n'.")
        new_password = generate_password(platform, password=password)
        return new_password


def add_account(id):
    """
    Prompts the user to enter a new password for a website/application
    and saves it into their respective passwords.json file.
    """

    platform = (
        input("Enter the platform (e.g., website, application): ")).lower()
    username = input("Enter the username: ")
    new_password = generate_password(platform)
    encrypted_password = encrypt(new_password)

    data = {
        platform: {'username': username,
                   'password': encrypted_password}
    }

    try:
        with open(f"{id}saved_passwords.json", "r+") as f:
            try:
                saved_passwords = json.load(f)
            except json.JSONDecodeError:
                saved_passwords = {}

            saved_passwords.update(data)
            f.seek(0)
            json.dump(saved_passwords, f, indent=4)

    except FileNotFoundError:
        with open(f"{id}saved_passwords.json", "w") as f:
            json.dump(data, f, indent=4)

    print("Password saved successfully.")
    start(id)


def update_password(id):
    """
    Allows the user to update the password for a given platform and saves the updated password.
    """

    platform = (
        input("Enter the platform (e.g., website, application): ")).lower()

    if check_account(id, platform):
        new_password = generate_password(platform)
        encrypted_password = encrypt(new_password)

        try:
            with open(f"{id}saved_passwords.json", "r+") as f:
                try:
                    saved_passwords = json.load(f)
                except json.JSONDecodeError:
                    saved_passwords = {}

                if platform in saved_passwords:
                    saved_passwords[platform]['password'] = encrypted_password
                    f.seek(0)
                    json.dump(saved_passwords, f, indent=4)
                    print(f"Password for {platform} updated successfully.")
                else:
                    print(f"There is no account saved for {platform}. Make sure there are no spelling mistakes.")

        except FileNotFoundError:
            print("There are no saved passwords yet.")

        start(id)


def delete_account(id, platform):
    """
    Deletes the saved account info for the given platform from the user's passwords.json file.
    """

    if check_account(id, platform):
        check = (input(f"Are you sure you want to delete your saved credentials for {platform} [y/n]: ")).lower()

        if check == "y":

            try:
                with open(f"{id}saved_passwords.json", "r") as f:
                    saved_passwords = json.load(f)
                    del saved_passwords[platform]
                    with open(f"{id}saved_passwords.json", "w") as f:
                        json.dump(saved_passwords, f, indent=4)

            except FileNotFoundError:
                print("No saved passwords found. Please create a new account.")
                start(id)

            else:
                print("Account deleted successfully.")
                start(id)

        elif check == "n":
            start(id)

        else:
            print("Please enter 'y' or 'n'.")
            delete_account(id, platform)


def delete_user(id):
    check = (
        input("Are you sure you want to delete your user [y/n]: ")).lower()

    if check == "y":

        with open("credentials.json", "r") as f:
            credentials = json.load(f)
            del credentials[id]
            with open("credentials.json", "w") as f:
                json.dump(credentials, f, indent=4)

        try:
            os.remove(f"{id}saved_passwords.json")

        except FileNotFoundError:
            main()

        else:
            print("User deleted successfully.")
            main()

    elif check == "n":
        start(id)

    else:
        print("Please enter 'y' or 'n'.")
        delete_user(id)


def retrieve_account(id, platform):

    if check_account(id, platform):

        try:
            with open(f"{id}saved_passwords.json", "r") as f:
                saved_passwords = json.load(f)
                username, password = saved_passwords[platform].items()
                password = decrypt(password[1])

        except FileNotFoundError:
            print("No saved passwords found.")
            start(id)

        else:
            print(f"The username for {platform}: {username[1]}")
            print(f"The password for {platform}: {password[1]}")
            start(id)

    else:
        start(id)


def start(id):
    while True:
        check_reason = input(
            "Do you want to ...\n(1) add a new account\n(2) update an existing password\n(3) delete an account\n(4) retrieve an account\n(5) delete user\n(Press any other key to exit): ")
        if check_reason == '1':
            add_account(id)
        elif check_reason == '2':
            update_password(id)
        elif check_reason == '3':
            platform = (
                input("Which platform do you want to delete your info? ")).lower()
            delete_account(id, platform)
        elif check_reason == '4':
            platform = (
                input("Which platform do you want to retrieve your info? ")).lower()
            retrieve_account(id, platform)
        elif check_reason == '5':
            delete_user(id)
        else:
            print("Exiting...")
            break


def main():
    access = input("Press (1) to login or (2) to create a new account: ")
    if access == '1':
        status, id = login()
        if status:
            start(id)
        else:
            print("Access denied!")
            main()
    elif access == '2':
        create_user()
        main()
    else:
        print("Invalid input. Please try again.")
        main()


if __name__ == '__main__':
    main()
