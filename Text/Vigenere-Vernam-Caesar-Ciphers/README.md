# Vigenere / Vernam / Ceasar Ciphers

**Category:** Text

## Problem

Functions for encrypting and decrypting data messages. Then send them to a friend.

## Solution

Three classical ciphers in one CLI: Caesar shifts letters by 1-25 and wraps within each case; Vigenere applies a repeating letter key, advancing it only on letters; Vernam XORs UTF-8 bytes with a repeating key and Base64-encodes the ciphertext so it is safe to paste. Non-letters pass through the letter ciphers unchanged.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --cipher caesar --text "Attack at dawn" --key 3
python3 main.py --cipher vigenere --text "Attack at dawn" --key LEMON
python3 main.py --cipher vernam --mode decrypt --text "<base64>" --key s3cret
python3 main.py --demo
```

## Example

```text
caesar   key=3      encrypted=Dwwdfn dw gdzq!
         decrypted=Attack at dawn!  roundtrip=True
vigenere key=LEMON  encrypted=Lxfopv ef rnhr!
         decrypted=Attack at dawn!  roundtrip=True
vernam   key=s3cret encrypted=MkcXEwYfU1IXUgEVBF1C
         decrypted=Attack at dawn!  roundtrip=True
caesar key=20, 'HI' -> BC
```
