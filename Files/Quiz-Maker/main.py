#!/usr/bin/env python3
"""Build a random quiz from a question bank, grade it, and print an answer key."""
import argparse
import json
import random
import tempfile
import os

def load_questions(path: str):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    questions = data["questions"] if isinstance(data, dict) else data
    for index, question in enumerate(questions, 1):
        if not {"question", "options", "answer"} <= set(question):
            raise ValueError(f"question {index} needs question/options/answer")
        if not 0 <= int(question["answer"]) < len(question["options"]):
            raise ValueError(f"question {index} has an out-of-range answer")
    return questions

def build_quiz(questions, count: int, seed=None):
    rng = random.Random(seed)
    chosen = rng.sample(questions, min(count, len(questions)))
    quiz = []
    for question in chosen:
        options = list(question["options"])
        correct_text = options[int(question["answer"])]
        rng.shuffle(options)
        quiz.append({"question": question["question"], "options": options,
                     "answer": options.index(correct_text)})
    return quiz

def grade(quiz, responses):
    """Return (score, details); responses maps question index to chosen index."""
    details = []
    score = 0
    for index, item in enumerate(quiz):
        chosen = responses.get(index)
        correct = chosen == item["answer"]
        score += correct
        details.append((index + 1, item["question"], chosen, item["answer"], correct))
    return score, details

QUESTIONS = {
    "questions": [
        {"question": "Which data structure uses FIFO order?", "options": ["Stack", "Queue", "Tree", "Set"], "answer": 1},
        {"question": "What is the time complexity of binary search?", "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"], "answer": 1},
        {"question": "Which Python type is immutable?", "options": ["list", "dict", "tuple", "set"], "answer": 2},
        {"question": "What does SQL stand for?", "options": ["Structured Query Language", "Simple Query Logic", "Sequential Query Layer", "Standard Question Language"], "answer": 0},
        {"question": "Which HTTP status means Not Found?", "options": ["200", "301", "404", "500"], "answer": 2},
    ]
}

def demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "questions.json")
        json.dump(QUESTIONS, open(path, "w"))
        questions = load_questions(path)
        quiz = build_quiz(questions, 3, seed=7)
        responses = {index: item["answer"] for index, item in enumerate(quiz)}
        score, details = grade(quiz, responses)
        for number, text, chosen, answer, correct in details:
            print(f"{number}. {text} -> {'correct' if correct else 'wrong'}")
        print(f"score: {score}/{len(quiz)}")
        print("answer key:", [item["answer"] + 1 for item in quiz])

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", help="JSON question bank")
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo or not args.file:
        demo(); return
    quiz = build_quiz(load_questions(args.file), args.count, args.seed)
    responses = {}
    for index, item in enumerate(quiz, 1):
        print(f"\n{index}. {item['question']}")
        for letter, option in zip("abcd", item["options"]):
            print(f"   {letter}) {option}")
        answer = input("answer: ").strip().lower()[:1]
        responses[index - 1] = "abcd".index(answer) if answer in "abcd" else -1
    score, details = grade(quiz, responses)
    print(f"\nscore: {score}/{len(quiz)}")
    for number, text, chosen, answer, correct in details:
        if not correct:
            print(f"  {number}: correct answer was {answer + 1}) {quiz[number-1]['options'][answer]}")

if __name__ == "__main__":
    main()
