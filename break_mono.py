import argparse
from crypto.io import IfStream
from crypto.mono import Cipher
from utils.spinner import Spinner

def main():
    # create arg parse instance
    parser = argparse.ArgumentParser()
    parser.add_argument('FILE', type=str, help='ciphertext which is used to derive the key')
    parser.add_argument('REFERENCE_DATA', type=str, help='reference data to analyze the ciphertext')

    # parse arguments
    args = parser.parse_args()

    # read file
    ciphertext = IfStream(args.FILE)
    refData = args.REFERENCE_DATA

    # derive key from ciphertext
    with Spinner('Analyzing cipher '):
        key = Cipher.deriveKey(ciphertext.data, refData)

    # print key to stdout
    print(f"The key is: {key}")


if __name__ == '__main__':
    main()
