# -*- coding: utf-8 -*-
import random
import pathlib
import os
import platform
from string import ascii_lowercase

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

NUM_QUESTIONS_PER_QUIZ = 5
QUESTIONS_DIR = pathlib.Path(__file__).parent / "questions"  # New: Directory for question files


def run_quiz():
    clear_console()
    questions = prepare_questions(QUESTIONS_DIR, num_questions=NUM_QUESTIONS_PER_QUIZ)

    num_correct = 0
    for num, question in enumerate(questions, start=1):
        print(f"\n*** Question {num} ***")
        # num_correct += ask_question(question)
        num_correct = ask_question(question)
        # print(f"You have {num_correct} correct answers.")

    print(f"\nYou got {num_correct} out of {num} questions.")


# preprocessing
def prepare_questions(questions_dir, num_questions):
    topics = {}
    for toml_file in questions_dir.glob("*.toml"):
        topic_info = tomllib.loads(toml_file.read_text(encoding="utf-8"))
        # Assume each file has one top-level section (e.g., [beverly_hills_90210])
        # for topic_key, topic_data in topic_info.items():
        for topic_data in topic_info.values():
            topics[topic_data["label"]] = topic_data["questions"]
    
    if not topics:
        raise ValueError(f"No question files found in {questions_dir}")
    
    topic_label = get_answers(
        "Which topic do you want to get quizzed about?",
        alternatives=sorted(topics),
    )[0]
    questions = topics[topic_label]
    num_questions = min(num_questions, len(questions))
    chosen_quiz_presentation(topic_label, num_questions)
    return random.sample(questions, k=num_questions)


def chosen_quiz_presentation(topic, num_questions):
    clear_console()
    print("\n******************************************************************")
    print(f"  Ok, you have chosen to be quized in topic: \n  {topic!r}")
    print(f"  The quiz have {num_questions} questions. Are you ready? ")
    print("********************************************************************")
    input("\n  Push 'Enter' button to go to the next question.")

def ask_question(question):
    correct_answers = question["answers"]
    alternatives = question["answers"] + question["alternatives"]
    ordered_alternatives = random.sample(alternatives, k=len(alternatives))

    answers = get_answers(
        question["question"],
        ordered_alternatives,
        num_choices=len(correct_answers),
        hint=question.get("hint"),
    )
    points = validate_answers(correct_answers, answers)
    print(f"You have {points} correct answers.")

    if "explanation" in question:
        print(f"\nExplanation:\n{question['explanation']}")
    
    input("\nPush 'Enter' button to go to the next question.")
    return points


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
    # Keep a running total of points across calls using function attribute
    if not hasattr(validate_answers, "total_points"):
        validate_answers.total_points = 0

    correct = set(answers) == set(correct_answers)
    if correct:
        print("\n⭐ Correct ⭐")
        validate_answers.total_points += 1
    else:
        print("\n❗Wrong❗")

    is_or_are = " is" if len(correct_answers) == 1 else "s are"
    print("\n- ".join([f"The answer{is_or_are}:"] + correct_answers))

    # return cumulative pointss, not just 0/1
    return validate_answers.total_points


def clear_console():
    """ clear the CommandPrompt/PowerShell """
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

if __name__ == "__main__":
    run_quiz()
