## 1) Starting point ###

# answer = input("When was the first known use of the word 'quiz'? ")
# if answer == "1781":
#     print("Correct!")
# else:
#     print(f"The answer is 1781, not {answer!r}")

# answer = input("Which built-in function can get information from the user? ")
# if answer == "input":
#     print("Correct!")
# else:
#     print(f"The answer is 'input', not {answer!r}")

### 2) Use Lists and Tuples to Avoid Repetitive Code ###

# QUESTIONS = [
#     ("When was the first known use of the word 'quiz'", "1781"),
#     ("Which built-in function can get information from the user", "input"),
#     ("Which keyword do you use to loop over a given list of elements", "for"),
# ]

# for question, correct_answer in QUESTIONS:
#     answer = input(f"{question}? ")
#     if answer == correct_answer:
#         print("Correct!")
#     else:
#         print(f"The answer is {correct_answer!r}, not {answer!r}")

### 3) Provide Multiple Choices ###

from string import ascii_lowercase

QUESTIONS = {
    "When was the first known use of the word 'quiz'": ["1781", "1771", "1871", "1881"],
    "Which built-in function can get information from the user": [
        "input",
        "get",
        "print",
        "write",
    ],
    "Which keyword do you use to loop over a given list of elements": [
        "for",
        "while",
        "each",
        "loop",
    ],
    "What's the purpose of the built-in zip() function": [
        "To iterate over two or more sequences at the same time",
        "To combine several strings into one",
        "To compress several files into one archive",
        "To get information from the user",
    ],
    "What's the name of Python's sorting algorithm": [
        "Timsort",
        "Quicksort",
        "Merge sort",
        "Bubble sort",
    ],
    "What does dict.get(key) return if key isn't found in dict": [
        "None",
        "key",
        "True",
        "False",
    ],
}

# for question, alternatives in QUESTIONS.items():
#     correct_answer = alternatives[0]  # antager at det rigtige svar er det første i listen.
#     sorted_answer = sorted(alternatives)
#     for label, alternative in enumerate(sorted_answer):
#         print(f"   - {label}) {alternative}")

#     answer_label = int(input(f"{question}? "))
#     answer = sorted_answer[answer_label]
#     if answer == correct_answer:
#         print("Correct!")
#     else:
#         print(f"The answer is {correct_answer!r}, not {answer!r}")

num_correct = 0  # tæller antal korekte svar.

for num, (question, alternatives) in enumerate(QUESTIONS.items(), start=1):
    print(f"\nQuestion: {num}:")
    print(f"{question}?")
    correct_answer = alternatives[
        0
    ]  # antager at det rigtige svar er det første i listen.
    labeled_alternatives = dict(zip(ascii_lowercase, sorted(alternatives)))
    for label, alternative in labeled_alternatives.items():
        print(f"   {label}) {alternative} ")

    answer_label = input("\nChoice (write the letter)? ")
    answer = labeled_alternatives.get(answer_label)

    if answer == correct_answer:
        num_correct += 1
        print(f"⭐ Correct ⭐\nThe answer is {correct_answer!r}.")
    else:
        print("❗Wrong❗")
        print(f"The answer is {correct_answer!r}, \n(Your answer: {answer!r})")
    go_to_next = input("\nPush any button to go to the next question.")

print(f"\nYou got {num_correct} out of {num} questions.")
