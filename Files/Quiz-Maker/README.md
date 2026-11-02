# Quiz Maker

**Category:** Files

## Problem

Make an application which takes various questions from a file, picked randomly, and puts together a quiz for students. Each quiz can be different and then reads a key to grade the quizzes.

## Solution

Loads a JSON question bank, samples N questions, and shuffles each question's options while tracking the correct option by text, so every generated quiz differs but grading stays exact. Interactive mode asks one question at a time; the demo auto-answers and prints a key.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --file questions.json --count 5 --seed 42
python3 main.py --demo
```

## Example

```text
1. Which Python type is immutable? -> correct
2. What is the time complexity of binary search? -> correct
3. What does SQL stand for? -> correct
score: 3/3
answer key: [2, 1, 3]
```
