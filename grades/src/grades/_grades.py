"""Egregiously over-engineered test score to letter grade utility

Originally intended to illustrate how to do that grading program
using bisect, expanding on the example from the bisect documentation

https://docs.python.org/3/library/bisect.html#examples

But then I started tinkering way to much.
"""

# bisect.bisect() does the magic, but it takes some practice,
# and the documentation isn't really clear to those who haven't
# tried to do this on their own first.
from bisect import bisect

# Mapping is just so I can give a proper type annotation for grade()
# Don't worry about it at this point. It roughly means a
# dict-like thing that is NOT mutable.
# Likewise Sequence is for list-like things that are immutable.
from collections.abc import Mapping, Sequence

# Because we want math.inf for full range of possible scores
import itertools
import math

# We will want to cache the __str__ result for a Grader instance
# But note that type checkers and @cache don't play nicely together.
# See https://stephantul.github.io/blog/cache/
import functools


class Grader:
    """Score to grade calculator.

    Can be used for any bijective step function, Callable[[float], str].
    """

    DEFAULT_MAP: Mapping[str, float] = {
        "F": 59,
        "D": 69,
        "C": 79,
        "B": 89,
        "A": math.inf,
    }
    """Default grade map."""

    def __init__(
        self,
        grades: Sequence[str] = "FDCBA",
        cutoffs: Sequence[float] = (60, 70, 80, 90),
        min_score: float = -math.inf,
        max_score: float = math.inf,
    ) -> None:
        """Defines the score to grade function.

        :param grades: A sorted list of grades
        :param cutoffs:
            A strictly sorted list of separation points between grades
            with each representing the lowest score for the grade
        :param min_score: The minimum possible score.
        :param max_score: The maximin possible score.


        :raises ValueError: if cutoffs are not strictly descending.
        :raises ValueError: if len(cutoffs) + 1 != len(grades)
        :raises ValueError: if grades has duplicate values.
        :raises ValueError: if lowest cutoff value is less than ``min_score``.
        :raises ValueError:
            if highest cutoff value is greater than ``min_score``.
        """
        self._grades = grades
        self._cutoffs = cutoffs[:]  # If user doesn't respect Sequence
        self._min_score = min_score
        self._max_score = max_score

        if len(self._grades) - 1 != len(cutoffs):
            raise ValueError(
                f"Number of cutoffs ({len(cutoffs)}) must be"
                f"one less than the number of grades ({len(grades)})"
            )

        if len(grades) != len(set(grades)):
            raise ValueError("grades cannot contain duplicates")

        if not all(
            [higher > lower for lower, higher in zip(cutoffs, cutoffs[1:])]
        ):
            raise ValueError("Cutoffs must be strictly ascending")

        if cutoffs[0] <= min_score:
            raise ValueError(
                f"lowest cutoff ({cutoffs[0]}) must be greater than "
                f"minimum allowed score ({min_score})"
            )
        if cutoffs[-1] >= max_score:
            raise ValueError(
                f"lowest cutoff ({cutoffs[-1]}) must be less than "
                f"maximum allowed score ({max_score})"
            )

    def grade(self, score: float) -> str:
        """Returns the grade for a particular score.

        :param score: The numeric score

        :raises ValueError: if score exceeds max_score.
        :raises ValueError: if score is less than min_score
        :raises ValueError: if score in not finite
        """
        if abs(score) == math.inf:
            raise ValueError("Score must be finite")
        if score < self._min_score:
            raise ValueError(f"Score ({score}) < minimum ({self._min_score})")

        if score > self._max_score:
            raise ValueError(f"Score ({score}) > maximum ({self._max_score})")

        # Now the magic bit
        # idx will be the index to the the first member of the cutoffs
        # array that that is not less than score
        idx = bisect(self._cutoffs, score)
        return self._grades[idx]

    @property
    def mapping(self) -> Mapping[str, float]:
        extended_cutoffs = itertools.chain(self._cutoffs, (self._max_score,))
        d: Mapping[str, float] = {
            g: c for g, c in zip(self._grades, extended_cutoffs)
        }
        return d

    @functools.cache
    def __str__(self) -> str:  # pyright: ignore
        s = f"Grade Mapping: {self.mapping}\n"
        s += f"Minimum allowed score: {self._min_score}\n"
        s += f"Maximum allowed score: {self._max_score}"

        return s
