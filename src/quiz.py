import random
import pathlib
from string import ascii_lowercase
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

NUM_QUESTIONS_PER_QUIZ = 5
QUESTIONS_PATH = pathlib.Path(__file__).parent / "questions.toml"
# QUESTIONS = tomllib.loads(QUESTIONS_PATH.read_text())


def run_quiz():
    questions = prepare_questions(
        QUESTIONS_PATH, num_questions=NUM_QUESTIONS_PER_QUIZ
    )

    num_correct = 0
    for num, question in enumerate(questions, start=1):
        print(f"\n*** Question {num} ***")
        num_correct += ask_question(question)

    print(f"\nYou got {num_correct} out of {num} questions.")


# preprocessing
def prepare_questions(path, num_questions):
    questions = tomllib.loads(path.read_text())["questions"]
    num_questions = min(num_questions, len(questions))
    return random.sample(list(questions.items()), k=num_questions)


def ask_question(question):
    # correct_answer = alternatives[0]
    correct_answer = question["answer"]
    # ordered_alternatives = random.sample(alternatives, k=len(alternatives))
    alternatives = question["answer"] + question["alternatives"]
    ordered_alternatives = random.sample(
        alternatives, k=len(alternatives)
    )

    answer = get_answer(question["question"], ordered_alternatives)
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
