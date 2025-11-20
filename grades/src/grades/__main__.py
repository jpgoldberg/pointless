import fileinput
import logging

from . import Grader

# Unlike _grader.py, this CLI is distinctly under-engineered.

# TODO: Add argument parsing and help


def main() -> None:
    grader = Grader()  # Just use default for now

    line_count = 0
    for line in fileinput.input(encoding="utf-8"):
        line_count += 1
        line = line.strip()
        try:
            score = int(line)
        except ValueError as e:
            logging.warning(f"Error on input line {line_count}: {e}")
        else:
            print(grader.grade(score))


if __name__ == "__main__":
    main()
