import tomllib

with open("questions.toml", mode="rb") as toml_file:
    questions = tomllib.load(toml_file)

questions
