import math
import sys
import unittest  # for unittest.TestCase.subTest
import pytest
from dataclasses import dataclass

import grades


@dataclass(frozen=True)
class ScoreVector:
    score: float
    grade: str
    exception: None | type[Exception] = None
    note: str | None = None


class TestDefault(unittest.TestCase):
    vectors: list[ScoreVector] = [
        ScoreVector(49, 'F', note="Normal"),
        ScoreVector(50, 'F', note="Normal"),
        ScoreVector(51, 'F', note="Normal"),

        ScoreVector(59, 'F', note="Normal"),
        ScoreVector(60, 'D', note="Normal"),
        ScoreVector(61, 'D', note="Normal"),

        ScoreVector(69, 'D', note="Normal"),
        ScoreVector(70, 'C', note="Normal"),
        ScoreVector(71, 'C', note="Normal"),

        ScoreVector(79, 'C', note="Normal"),
        ScoreVector(80, 'B', note="Normal"),
        ScoreVector(81, 'B', note="Normal"),

        ScoreVector(89, 'B', note="Normal"),
        ScoreVector(90, 'A', note="Normal"),
        ScoreVector(90, 'A', note="Normal"),

        ScoreVector(0, 'F'),
        ScoreVector(100, 'A'),

        ScoreVector(-1, 'F', note="Below 0"),
        ScoreVector(101, 'A', note="Above 100"),
        ScoreVector(math.inf, 'A', exception=ValueError, note="Not finite"),
        ScoreVector(-math.inf, 'F', exception=ValueError, note="Not finite"),
    ]  # fmt: skip

    def test_init(self) -> None:
        _ = grades.Grader()

    def test_normal(self) -> None:
        grader = grades.Grader()
        for v in self.vectors:
            if v.exception is not None:
                continue
            if not (v.note is None or v.note == "Normal"):
                continue
            with self.subTest(msg=f'score: {v.score}. Note: "{v.note}"'):
                grade = grader.grade(v.score)
                assert grade == v.grade

    def test_abnormal(self) -> None:
        grader = grades.Grader()
        for v in self.vectors:
            if v.exception is not None:
                continue
            if v.note is None or v.note == "Normal":
                continue
            with self.subTest(msg=f'score: {v.score}. Note: "{v.note}"'):
                grade = grader.grade(v.score)
                assert grade == v.grade

    def test_exceptions(self) -> None:
        grader = grades.Grader()
        for v in self.vectors:
            if v.exception is None:
                continue
            with self.subTest(msg=f'score: {v.score}. Note: "{v.note}"'):
                with pytest.raises(v.exception):
                    _ = grader.grade(v.score)


class TestGrader(unittest.TestCase):
    good_grades = "ABCDF"
    good_cutoffs = (60, 70, 80, 90)

    def test_duplicate_grades(self) -> None:
        bad_grades = "ABCDB"

        with pytest.raises(ValueError):
            _ = grades.Grader(grades=bad_grades, cutoffs=self.good_cutoffs)

    def test_min_mismatch(self) -> None:
        bad_min_scores = (self.good_cutoffs[0] + 1, self.good_cutoffs[0])
        for bad_min_score in bad_min_scores:
            with pytest.raises(ValueError):
                _ = grades.Grader(
                    grades=self.good_grades,    
                    cutoffs=self.good_cutoffs,
                    min_score=bad_min_score,
                )


if __name__ == "__main__":
    sys.exit(pytest.main(args=[__file__]))
