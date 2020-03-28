# Mono Cipher Suite
This cipher suite is a simple implementation of the mono-alphabetic substitution. The main purpose of this tool is to 
show you how to crack/derive the used substitution alphabet by using statistic analysis. 

## Features
- Encryption
- Decryption
- Key derivation (Get substitution alphabet from ciphertext)

## Usage
```
usage: mono.py [-h] (--encrypt KEY | --decrypt KEY) [--out OUT] FILE
```
### Encryption
Example: Encrypt content of *plaintext.txt* with *rehmtfzgoxsqwpclbanjdykuiv* and save in file *cipher.txt*
```
python mono.py --encrypt rehmtfzgoxsqwpclbanjdykuiv plaintext.txt --out cipher.txt
```

### Decryption
Example: Decrypt content of *cipher.txt* with *rehmtfzgoxsqwpclbanjdykuiv* and save in file *plaintext.txt*
```
python mono.py --decrypt rehmtfzgoxsqwpclbanjdykuiv plaintext.txt --out cipher.txt
```

### Key Derivation
```
usage: break_mono.py [-h] FILE REFERENCE_DATA
```

Example: Derive key from cipher *cipher.txt* using King James Bible as reference statistics
```
python break_mono.py cipher.txt king_james.txt
```