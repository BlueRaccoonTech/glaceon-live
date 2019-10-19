import os
import sys
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
import feapp.data.db_session as db_session
from feapp.data.users import User
from feapp.data.userData import UserData
from feapp.data.userKeys import UserKeys
from feapp.data.userKeys import genstreamkey
import getpass

# Make it run more easily outside of PyCharm
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..")))


def main():
    init_db()
    while True:
        create_user()


def hash_text(text: str) -> str:
    hashed_text = crypto.encrypt(text, rounds=171204)
    return hashed_text


def create_user():
    new_user = User()
    new_user.username = input('Username: ').strip().lower()
    new_user.email = input("E-mail Address: ").strip()
    new_user.hashed_password = hash_text(input("Password: ").strip())

    new_user_info = UserData()
    new_user_info.displayName = input("Display Name: ")
    new_user_info.tagline = input("Tagline: ")
    new_user_info.description = input("Description: ")
    new_user_info.username = new_user.username

    new_user_key = UserKeys()
    new_user_key.streamingKey = genstreamkey()
    new_user_key.username = new_user.username

    session = db_session.create_session()
    session.add(new_user)
    session.add(new_user_info)
    session.add(new_user_key)
    session.commit()


def init_db():
    top_folder = os.path.dirname(__file__)
    rel_file = os.path.join('..', 'db', 'glaceon.sqlite')
    db_file = os.path.abspath(os.path.join(top_folder, rel_file))
    db_session.global_init(db_file)


if __name__ == '__main__':
    main()
