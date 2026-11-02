# Pig Latin

**Category:** Text

## Problem

Pig Latin is a game of alterations played on the English language game. To create the Pig Latin form of an English word the initial consonant sound is transposed to the end of the word and an ay is affixed (Ex.: "banana" would yield anana-bay). Read Wikipedia for more information on rules.

## Solution

Moves the leading consonant cluster to the end and appends "ay"; words starting with a vowel get "way" instead. Capitalization, leading punctuation (quotes/brackets) and trailing punctuation are preserved, and vowel-less words are handled safely (treating y as a consonant).

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py "Hello world"
python3 main.py --demo
```

## Example

```text
'banana' -> 'ananabay'
           'Hello world' -> 'Ellohay orldway'
                 'apple' -> 'appleway'
       'Sky, the rhythm!' -> 'Skyay, ethay rhythmay!'
          'STRONG words' -> 'ONGSTRAY ordsway'
        'Pig Latin is fun' -> 'Igpay Atinlay isway unfay'
```
