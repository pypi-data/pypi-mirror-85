import sys
import os
import argparse

from .core import Tenc


def main(args=None):
    parser = argparse.ArgumentParser(description='Encrypt and decrypt files')

    parser.add_argument('-f', dest='path', help='Path to file', required=True)
    parser.add_argument('-p', dest='password', help='The password', required=True)
    parser.add_argument('-d', action='store_true', help='Should decrypt otherwise encrypt')

    args = parser.parse_args()

    TencInstance = Tenc()

    if not args.d:
        filename = args.path + '.enc'

        with open(args.path, 'r') as plainFile:
            with open(filename, 'w') as f:
                f.write(TencInstance.encrypt(plainFile.read(), args.password))
                print('{} encrypted and saved as {}'.format(args.path, filename))
                f.close()

            plainFile.close()
    else:
        filename = os.path.join(os.path.dirname(args.path), 'dec_' + os.path.basename(args.path).replace('.enc', ''))

        with open(args.path, 'r') as encryptedFile:
            with open(filename, 'w') as f:
                decrypted = TencInstance.decrypt(encryptedFile.read(), args.password)
                if decrypted:
                    f.write(decrypted)
                    print('{} decrypted and saved as {}'.format(args.path, filename))
                f.close()

            encryptedFile.close()


if __name__ == "__main__":
    sys.exit(main())
