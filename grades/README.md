# Over-engineered Python grade calculator (with bisect)

A familiar beginner exercise for handling multiple conditions often
presented as something like
(modified from
[Exercism subproblem](https://exercism.org/tracks/python/exercises/making-the-grade))

> The teacher you are assisting likes to assign letter grades as well as numeric scores.
> Since students rarely score 100 on an exam, the "letter grade" lower thresholds are calculated based on the highest score achieved [...]
>
> Create the function letter_grades(score) that takes the
> score on the exam as an argument, and returns a list of lower
> score thresholds for each "American style" grade interval: ["D", "C", "B", "A"].

And the problem then includes the score ranges for each letter grade.

This exercise is used to force people to get used to using
the `if ... elif ... else` construction for the language.
The exercise offers some scope for learners to provide versions with less repetition
of the score cutoffs. And it might even prompt some students to thing,
"there has to be a better way".

## What prompted me to make this

The world does not need yet another implementation of this beginner exercise,
and what I have here is not suitable learning material for the
the person just learning about conditionals. Yet I made it.

One learner I know was presented with a variation of this problem in which
the problem was stated with a gap in the grade ranges. I don't know if that
was deliberately done by the instructor. I suspect it was.

My response when told about this was something along the lines of,
"Oh, there is a really cool way to both avoid all of the `elif`s and
prevent any accidental gaps or overlap of ranges, but you aren't ready for that yet."

Still I wanted to illustrate the use of Python's `bisect` for this, but I also found
the example in the Python documentation unsatisfactory as it assumes a lot of things about its
input cutoffs and grades.

That is where I started. What you see is where this currently is.
