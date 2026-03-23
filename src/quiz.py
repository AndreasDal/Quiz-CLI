import random
import pathlib
from string import ascii_lowercase
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

NUM_QUESTIONS_PER_QUIZ = 5
QUESTIONS_PATH = pathlib.Path(__file__).parent / "questions.toml"
QUESTIONS = tomllib.loads(QUESTIONS_PATH.read_text())


# QUESTIONS = {
#     "When was the first known use of the word 'quiz'": ["1781", "1771", "1871", "1881"],
#     "Which built-in function can get information from the user": [
#         "input",
#         "get",
#         "print",
#         "write",
#     ],
#     "Which keyword do you use to loop over a given list of elements": [
#         "for",
#         "while",
#         "each",
#         "loop",
#     ],
#     "What's the purpose of the built-in zip() function": [
#         "To iterate over two or more sequences at the same time",
#         "To combine several strings into one",
#         "To compress several files into one archive",
#         "To get information from the user",
#     ],
#     "What's the name of Python's sorting algorithm": [
#         "Timsort",
#         "Quicksort",
#         "Merge sort",
#         "Bubble sort",
#     ],
#     "What does dict.get(key) return if key isn't found in dict": [
#         "None",
#         "key",
#         "True",
#         "False",
#     ],
# }


def run_quiz():
    questions = prepare_questions(
        QUESTIONS, num_questions=NUM_QUESTIONS_PER_QUIZ
    )

    num_correct = 0
    for num, (question, alternatives) in enumerate(questions, start=1):
        print(f"\n*** Question {num} ***")
        num_correct += ask_question(question, alternatives)

    print(f"\nYou got {num_correct} out of {num} questions.")


# preprocessing
def prepare_questions(questions, num_questions):
    num_questions = min(num_questions, len(questions))
    return random.sample(list(questions.items()), k=num_questions)


def ask_question(question, alternatives):
    correct_answer = alternatives[0]
    ordered_alternatives = random.sample(alternatives, k=len(alternatives))

    answer = get_answer(question, ordered_alternatives)
    point = validate_answer(correct_answer, answer)

    input("\nPush 'Enter' button to go to the next question.")
    return point


def get_answer(question, alternatives):
    print(f"{question}? ")
    labeled_alternatives = dict(zip(ascii_lowercase, alternatives))
    for label, alternative in labeled_alternatives.items():
        print(f"   {label}) {alternative}")

    while (
        answer_label := input("\nChoice (enter label)? ")
    ) not in labeled_alternatives:
        print(f"Please answer one of {', '.join(labeled_alternatives)}")

    return labeled_alternatives[answer_label]


def validate_answer(correct_answer, answer):
    if answer == correct_answer:
        print(f"⭐ Correct ⭐\nThe answer is {correct_answer!r}.")
        point = 1
    else:
        print("❗Wrong❗")
        print(f"The answer is {correct_answer!r}, \n(Your answer: {answer!r})")
        point = 0
    return point


if __name__ == "__main__":
    run_quiz()
