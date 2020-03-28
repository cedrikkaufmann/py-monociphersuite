import argparse
from crypto.io import IfStream
from crypto.mono import Cipher


def main():
    # create arg parse instance
    parser = argparse.ArgumentParser()
    parser.add_argument('FILE', type=str, help='file to encrypt/decrypt')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--encrypt', action='store', dest='ENCRYPT', metavar='KEY', type=str,
                       help='encrypt file using specified key')
    group.add_argument('--decrypt', action='store', dest='DECRYPT', metavar='KEY', type=str,
                       help='decrypt file using specified key')
    parser.add_argument('--out', action='store', dest='OUT', type=str,
                        help='save encrypted/decrypted file to specified one instead of printing to stdout')

    # parse arguments
    args = parser.parse_args()

    # read file
    f = IfStream(args.FILE)
    data = ''

    # check for encrypt/decrypt mode
    if args.ENCRYPT != None:
        # encrypt file content
        cipher = Cipher(args.ENCRYPT)
        data = cipher.encrypt(f.data)

    else:
        # decrypt file content
        cipher = Cipher(args.DECRYPT)
        data = cipher.decrypt(f.data)

    # check if result should be saved to file
    if args.OUT != None:
        # save result to file
        try:
            ofStream = open(args.OUT, 'w')
            ofStream.write(data)

        finally:
            # finally close file
            ofStream.close()
    else:
        # print result to stdout
        print(data)


if __name__ == '__main__':
    main()
