# Caesar cipher

**Category:** Security

## Problem

Implement a Caesar cipher, both encoding and decoding. The key is an integer from 1 to 25. This cipher rotates the letters of the alphabet (A to Z). The encoding replaces each letter with the 1st to 25th next letter in the alphabet (wrapping Z to A). So key 2 encrypts "HI" to "JK", but key 20 encrypts "HI" to "BC". This simple "monoalphabetic substitution cipher" provides almost no security, because an attacker who has the encoded message can either use frequency analysis to guess the key, or just try all 25 keys.

## Solution

Implements the cipher with case-preserving rotation, validates the 1-25 key range, and includes the two attacks the problem mentions: brute force over all 25 keys and a chi-squared frequency scorer that picks the most English-looking plaintext. The demo shows both attacks recovering the key.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --mode encode --text "Attack at dawn" --key 3
python3 main.py --mode decode --text "Dwwdfn dw gdzq" --key 3
python3 main.py --mode crack --text "Dwwdfn dw gdzq"
python3 main.py --mode brute --text "Dwwdfn dw gdzq"
python3 main.py --demo
```

## Example

```text
key 2:  HI -> JK
key 20: HI -> BC
encrypted: Esp bftnv mczhy qzi ufxad zgpc esp wlkj ozr
decrypted: The quick brown fox jumps over the lazy dog
cracked key=11 -> The quick brown fox jumps over the lazy dog
brute force (first 3): [(1, 'Cvvcem cv fcyp'), (2, 'Buubdl bu ebxo'), (3, 'Attack at dawn')]
```
