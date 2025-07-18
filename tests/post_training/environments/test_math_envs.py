import pytest

from marin.post_training.environments.math_utils import grade_answer


@pytest.mark.skip(reason="Need to fix environment import.")
def test_math_env_loaded():
    """Test whether MathEnv examples are loaded correctly."""
    from marin.post_training.environments.math_env import MathEnv

    math_env = MathEnv(tokenizer=None)
    assert len(math_env.train_examples) == 7500, "MathEnv train examples should not be empty"
    assert len(math_env.eval_examples) == 5000, "MathEnv eval examples should not be empty"


@pytest.mark.skip(reason="Need to fix environment import.")
def test_olym_math_env_loaded():
    """Test whether OlymMathEnv examples are loaded correctly."""
    from marin.post_training.environments.olym_math_env import OlymMathEnv

    olymp_math_env = OlymMathEnv(tokenizer=None, difficulty="easy", language="en")
    assert len(olymp_math_env.train_examples) == 80
    assert len(olymp_math_env.eval_examples) == 20

    # Ensure we get the same examples every time we load the environment
    assert olymp_math_env.train_examples[32]["prompt"].startswith(
        "Suppose 40 people vote anonymously, each with one ballot. "
        "Each person can vote for one or two candidates among three candidates. There are no invalid ballots"
    )
    assert olymp_math_env.eval_examples[16]["prompt"].startswith(
        "A frisbee toy is a circular disc divided into 20 sectors by 20 rays emanating from the center, "
        "with each sector colored either red or blue (only the front side is colored), and any two opposite "
        "sectors are colored differently. If frisbee toys that are the same after rotation are considered "
        "identical, how many different frisbee toys are there in total? (Answer with a specific number.)"
    )

    hard_olymp_math_env = OlymMathEnv(tokenizer=None, difficulty="hard", language="en")
    assert len(hard_olymp_math_env.train_examples) == 80
    assert len(hard_olymp_math_env.eval_examples) == 20
    assert hard_olymp_math_env.eval_examples[16]["prompt"].startswith(
        "If the inequality $2\\sin^2 C + \\sin A \\cdot \\sin B > k \\sin B \\cdot \\sin C$ holds for any "
        "triangle $\\triangle ABC$, find the maximum value of the real number $k$."
    )


@pytest.mark.skip(reason="Need to fix environment import.")
def test_open_math_reasoning_env_loaded():
    from marin.post_training.environments.open_math_reasoning_env import OpenMathReasoningEnv

    env = OpenMathReasoningEnv(tokenizer=None)
    assert len(env.train_examples) == 234_572
    assert len(env.eval_examples) == 1000

    # Ensure we get the same examples every time we load the environment
    assert env.train_examples[0]["prompt"].startswith(
        "Solve for \\( x \\): \\( |ax - 2| \\geq bx \\) given \\( a > 0 \\) and \\( b > 0 \\)"
    )
    assert env.train_examples[0]["answer"] == (
        "\\( x \\geq \\frac{2}{a-b} \\) or \\( x \\leq \\frac{2}{a+b} \\) or \\( x \\leq 0 \\)"
    )
    assert env.eval_examples[16]["prompt"].startswith(
        "For an integer \\( a > 1 \\) that is not a prime number, find the maximum possible "
        "value of \\( \\frac{a}{p^2} \\) where \\( p \\) is the smallest prime divisor of \\( a \\)."
    )


@pytest.mark.skip(reason="Need to fix environment import.")
def test_numina_math_env_loaded():
    from marin.post_training.environments.numina_math_env import NuminaMathEnv

    env = NuminaMathEnv(tokenizer=None)

    assert len(env.train_examples) == 836_291
    assert len(env.eval_examples) == 98

    # Ensure we get the same examples every time we load the environment
    assert env.train_examples[0]["prompt"].startswith(
        "Consider the terms of an arithmetic sequence: $-\\frac{1}{3}, y+2, 4y, \\ldots$. Solve for $y$."
    )
    assert env.eval_examples[16]["prompt"].startswith(
        "Given that the sequence $\\{a_n\\}$ is an arithmetic sequence, if $a_3 + a_{11} = 24$ and "
        "$a_4 = 3$, then the common difference of the sequence $\\{a_n\\}$ is ______."
    )


@pytest.mark.skip(reason="Need to fix environment import.")
def test_grade_answer_with_olym_math_env():
    """
    Test whether `grade_answer` works correctly with OlymMathEnv
    by ensuring a solution for one of the examples is verifiable.
    """
    from marin.post_training.environments.olym_math_env import OlymMathEnv

    hard_olymp_math_env = OlymMathEnv(tokenizer=None, difficulty="hard", language="en")

    example = hard_olymp_math_env.eval_examples[16]
    assert grade_answer(given_answer="2\\sqrt{2}-1", ground_truth=example["answer"]) is True
    assert grade_answer(given_answer=r"2\sqrt{2}-1", ground_truth=example["answer"]) is True
    assert grade_answer(given_answer=r"2*\sqrt{2} - 1", ground_truth=example["answer"]) is True
    assert grade_answer(given_answer=r"-1+2\sqrt{2}", ground_truth=example["answer"]) is True

    assert grade_answer(given_answer=r"2\sqrt{3}-1", ground_truth=example["answer"]) is False
    assert grade_answer(given_answer=r"2\sqrt{2} + 1", ground_truth=example["answer"]) is False


@pytest.mark.skip(reason="Need to fix environment import.")
def test_grade_answer_with_open_math_reasoning_env():
    """
    Test whether `grade_answer` works correctly with OpenMathReasoningEnv
    by ensuring a solution for one of the examples is verifiable.
    """
    from marin.post_training.environments.open_math_reasoning_env import OpenMathReasoningEnv

    env = OpenMathReasoningEnv(tokenizer=None)

    answer = env.train_examples[0]["answer"]
    assert (
        grade_answer(
            given_answer="\\( x \\geq \\frac{2}{a-b} \\) or \\( x \\leq \\frac{2}{a+b} \\) or \\( x \\leq 0 \\)",
            ground_truth=answer,
        )
        is True
    )
    assert (
        grade_answer(
            given_answer="\\( x \\geq \\frac{2}{a-b} \\), \\( x \\leq \\frac{2}{a+b} \\), \\( x \\leq 0 \\)",
            ground_truth=answer,
        )
        is True
    )
    assert (
        grade_answer(
            given_answer="\\( x \\geq \\frac{2}{a-b} \\) or \\( x \\leq \\frac{2}{a+b} \\) or \\( x \\geq 0 \\)",
            ground_truth=answer,
        )
        is False
    )

    answer = env.train_examples[1]["answer"]
    assert grade_answer(given_answer=" 20", ground_truth=answer) is True
    assert grade_answer(given_answer=" 19", ground_truth=answer) is False

    answer = env.train_examples[2]["answer"]
    assert grade_answer(given_answer="\\(-\\frac{2}{3}\\)", ground_truth=answer) is True
    assert grade_answer(given_answer="-\\frac{2}{3}", ground_truth=answer) is True
    assert grade_answer(given_answer="\\(-\\frac{4}{3}\\)", ground_truth=answer) is False
    assert grade_answer(given_answer="-\\frac{1}{3}", ground_truth=answer) is False


@pytest.mark.skip(reason="Need to fix environment import.")
def test_grade_answer_with_numina_math_env():
    from marin.post_training.environments.numina_math_env import NuminaMathEnv

    env = NuminaMathEnv(tokenizer=None)

    answer = env.train_examples[0]["answer"]
    assert grade_answer(given_answer="\\frac{13}{6}", ground_truth=answer) is True
    assert grade_answer(given_answer="+\\frac{13}{6}", ground_truth=answer) is True
    assert grade_answer(given_answer="-\\frac{13}{6}", ground_truth=answer) is False
