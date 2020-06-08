#!/usr/bin/env python3
import getpass
import argparse


def encrypt_file(file_name, key):
    from cryptography.fernet import Fernet
    with open(file_name, 'rb') as in_file:
        data = in_file.read()
    f = Fernet(key)
    data_encrypted = f.encrypt(data)
    with open(file_name, 'wb') as out_file:
        out_file.write(data_encrypted)


def decrypt_file(file_name, key):
    from cryptography.fernet import Fernet
    with open(file_name, 'rb') as in_file:
        data = in_file.read()
    f = Fernet(key)
    data_decrypted = f.decrypt(data)
    with open(file_name, 'wb') as out_file:
        out_file.write(data_decrypted)


def generate_key(password):
    import base64
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    import os
    if os.path.isfile('salt'):
        with open('salt', 'rb') as salt_file:
            salt = salt_file.read()
    else:
        with open('salt', 'wb+') as salt_file:
            salt = os.urandom(16)
            salt_file.write(salt)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def open_locked_file(args, key):
    import os
    from subprocess import call
    editor = os.environ.get('EDITOR', 'vim')
    if len(args.FILES) != 1:
        raise Exception('You can open only one file\n')

    decrypt_file(args.FILES[0], key)

    with open(args.FILES[0], 'a') as tf:
        tf.flush()
        call([editor, args.FILES[0]])
    encrypt_file(args.FILES[0], key)


def password_get():
    key = getpass.getpass(prompt='Password:', stream=None)
    if key == getpass.getpass(prompt='Again:', stream=None):
        return key
    else:
        raise Exception("Passwords doesn't match\n")


def process_args():
    parser = argparse.ArgumentParser(description='Encrypt and decrypt files.')
    parser.add_argument('-e', '--encrypt',
                        action='store_true',
                        help='''Encrypt files. (default)''')
    parser.add_argument('-d', '--decrypt',
                        action='store_true',
                        help='''Decrypt files.''')
    parser.add_argument('-o', '--open',
                        action='store_true',
                        help='''Open an encrypted file.''')
    parser.add_argument('-k', '--key',
                        action='store',
                        help='''Use key instead of password''')
    parser.add_argument('FILES',
                        nargs="*",
                        help='Files to process')
    args = parser.parse_args()

    if args.encrypt and args.decrypt:
        raise Exception("You can't use encrypt and decrypt together")

    return args


def main():
    args = process_args()

    if args.key:
        key = args.key
    else:
        password = password_get()
        key = generate_key(password)

    if args.open:
        open_locked_file(args, key)
    else:
        for item in args.FILES:
            if args.decrypt:
                decrypt_file(item, key)
            else:
                encrypt_file(item, key)


if __name__ == '__main__':
    main()
