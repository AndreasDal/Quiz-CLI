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
    questions = prepare_questions(QUESTIONS_PATH, num_questions=NUM_QUESTIONS_PER_QUIZ)

    num_correct = 0
    for num, question in enumerate(questions, start=1):
        print(f"\n*** Question {num} ***")
        num_correct += ask_question(question)

    print(f"\nYou got {num_correct} out of {num} questions.")


# preprocessing
def prepare_questions(path, num_questions):
    questions = tomllib.loads(path.read_text())["questions"]
    num_questions = min(num_questions, len(questions))
    # return random.sample(list(questions.items()), k=num_questions)
    return random.sample(questions, k=num_questions)


def ask_question(question):
    # correct_answer = alternatives[0]
    correct_answers = question["answers"]
    alternatives = question["answers"] + question["alternatives"]
    ordered_alternatives = random.sample(alternatives, k=len(alternatives))

    answers = get_answers(
        question["question"],
        ordered_alternatives,
        num_choices=len(correct_answers),
        hint=question.get("hint"),
    )
    point = validate_answers(correct_answers, answers)

    if "explanation" in question:
        print(f"\nExplanation:\n{question['explanation']}")
    
    input("\nPush 'Enter' button to go to the next question.")
    return point


def get_answers(question, alternatives, num_choices=1, hint=None):
    print(f"{question}? ")
    labeled_alternatives = dict(zip(ascii_lowercase, alternatives))
    if hint:
        labeled_alternatives["?"] = "Hint"

    for label, alternative in labeled_alternatives.items():
        print(f"   {label}) {alternative}")

    while True:
        plural_s = "" if num_choices == 1 else f"s (choose {num_choices})"
        answer = input(f"\nChoice{plural_s}? ")
        answers = set(answer.replace(",", " ").split())

        # Handle hints
        if hint and "?" in answers:
            print(f"\nHint: {hint}")
            continue
        
        # Handle involid andswers
        if len(answers) != num_choices:
            plural_s = "" if num_choices == 1 else "s, separated by comma"
            print(f"Please answer {num_choices} alternative{plural_s}")
            continue

        if any((invalid := answer) not in labeled_alternatives for answer in answers):
            print(
                f"{invalid!r} is not a valid choice. "
                f"Please use {', '.join(labeled_alternatives)}"
            )
            continue

        return [labeled_alternatives[answer] for answer in answers]


def validate_answers(correct_answers, answers):
    # if set(answers) == set(correct_answers):
    if correct := (set(answers) == set(correct_answers)):
        # print(f"⭐ Correct ⭐\nThe answer is {correct_answers!r}.")
        print("\n⭐ Correct ⭐")
        # point = 1
    else:
        # is_or_are = " is" if len(correct_answers) == 1 else "s are"
        print("\n❗Wrong❗")
        # print("\n- ".join(f"No, the answer{is_or_are} {correct_answers!r}, \n(Your answer: {answers!r})")
        # print("\n- ".join([f"No, the answer{is_or_are}:"] + correct_answers))
        # point = 0

    is_or_are = " is" if len(correct_answers) == 1 else "s are"
    print("\n- ".join([f"The answer{is_or_are}:"] + correct_answers))
    # return point
    return 1 if correct else 0


if __name__ == "__main__":
    run_quiz()
