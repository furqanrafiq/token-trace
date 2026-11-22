"""A tiny next-token predictor, to show what an LLM does at its core.

It learns which word tends to follow which from a small text, then
generates by repeating: score candidates, pick one, append, repeat.

A real LLM does the same loop with a neural network and billions of
parameters instead of a count table. Run: python next_token.py
"""
import random
from collections import Counter, defaultdict

TEXT = """
the capital of france is paris . the capital of italy is rome .
the capital of spain is madrid . the capital of france is paris .
paris is a city on the seine . rome is a city on the tiber .
madrid is a city in spain . the capital of japan is tokyo .
the capital of france is paris . the capital of france is paris .
people say the capital of france is lyon . paris is the capital of france .
""".split()
ORDER = 3  # how many previous tokens the model looks at (its "context")

# 1. "Training": count which token follows which.
follows = defaultdict(Counter)
for i in range(len(TEXT) - ORDER):
    follows[tuple(TEXT[i:i + ORDER])][TEXT[i + ORDER]] += 1


def scores(context, top=5):
    """Score every candidate next token as a probability."""
    counts = follows[tuple(context[-ORDER:])]
    total = sum(counts.values())
    return [(tok, c / total) for tok, c in counts.most_common(top)]


def generate(prompt, steps=8, seed=0, greedy=False):
    rng = random.Random(seed)
    tokens = prompt.split()
    for _ in range(steps):
        cands = scores(tokens)
        if not cands:
            break
        if greedy:
            pick = cands[0][0]
        else:
            pick = rng.choices([t for t, _ in cands], [p for _, p in cands])[0]
        tokens.append(pick)  # 2. add it to the text, 3. repeat
    return " ".join(tokens)


if __name__ == "__main__":
    prompt = "the capital of france is"
    print(f"Prompt: {prompt!r}\n")
    print("Candidates for the next token:")
    for tok, p in scores(prompt.split()):
        print(f"  {tok:<8} {p:5.0%}")
    print("\nMost likely path:  ", generate(prompt, greedy=True))
    print("Sampled (seed 1):  ", generate(prompt, seed=1))
    print("Sampled (seed 2):  ", generate(prompt, seed=2))
    print(
        "\nIt picks what is likely in its text, not what is true. "
        "Change TEXT and the 'facts' change."
    )
