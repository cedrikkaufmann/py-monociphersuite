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

#### Method
The key derivation is done in two phases. 

##### Phase 1
In the first phase an initial key is derived simply by the unigram
distribution given from the reference statistics. Therefore it is assumed that the character which is most likely to 
occur in the cipher would be the same as in the reference text. This is done in descending order for every character.

##### Phase 2
In this phase the key given from the previous phase is optimized by using a Maximum-Likelihood approach.
The key is optimized by randomly swapping two characters from the initial  
key alphabet. Next the cipher is decrypted using the new key and a fitness score is calculated. If the fitness score is
better for the key than the previous one. The newly obtained key is assumed to be the correct one.
This is done until a certain convergence criteria is met. This is given by "no better key in the last 2000 iterations".

## License
MIT licensed 2020 Cedrik Kaufmann. See the LICENSE file for further details.