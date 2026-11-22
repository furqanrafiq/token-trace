"""A tiny next-token predictor, to show what an LLM does at its core.

It learns which token tends to follow which from a small text, then
generates by repeating: score candidates, pick one, append, repeat.

A real LLM does the same loop with a neural network and billions of
parameters instead of a count table.

Usage:
    python next_token.py                      demo, then type your own prompts
    python next_token.py --prompt "the capital of italy is"
    python next_token.py --text mytext.txt    learn from your own text file
"""
import argparse
import random
import re
from collections import Counter, defaultdict

DEFAULT_TEXT = """
the capital of france is paris . the capital of italy is rome .
the capital of spain is madrid . the capital of france is paris .
paris is a city on the seine . rome is a city on the tiber .
madrid is a city in spain . the capital of japan is tokyo .
the capital of france is paris . the capital of france is paris .
people say the capital of france is lyon . paris is the capital of france .
the capital of germany is berlin . berlin is a city on the spree .
the capital of egypt is cairo . cairo is a city on the nile .
"""

ORDER = 3  # how many previous tokens the model looks at (its "context")


def tokenize(text):
    """Lowercase, and treat punctuation as its own token."""
    return re.findall(r"[a-z0-9']+|[.,!?;:]", text.lower())


def train(tokens):
    """'Training': count which token follows each context of 1..ORDER tokens."""
    follows = defaultdict(Counter)
    for n in range(1, ORDER + 1):
        for i in range(len(tokens) - n):
            follows[tuple(tokens[i:i + n])][tokens[i + n]] += 1
    return follows


def scores(follows, context, top=5):
    """Score every candidate next token. Falls back to a shorter context."""
    for n in range(min(ORDER, len(context)), 0, -1):
        counts = follows.get(tuple(context[-n:]))
        if counts:
            total = sum(counts.values())
            return [(t, c / total) for t, c in counts.most_common(top)]
    return []


def generate(follows, prompt, steps=8, seed=0, greedy=False):
    rng = random.Random(seed)
    tokens = list(prompt)
    for _ in range(steps):
        cands = scores(follows, tokens)
        if not cands:
            break
        if greedy:
            pick = cands[0][0]
        else:
            pick = rng.choices([t for t, _ in cands], [p for _, p in cands])[0]
        tokens.append(pick)  # add it to the text, then repeat
    return " ".join(tokens)


def show(follows, vocab, prompt_text):
    prompt = tokenize(prompt_text)
    if not prompt:
        return
    unknown = [t for t in prompt if t not in vocab]
    if unknown:
        print(f"  I have never seen: {', '.join(unknown)}. Try words from the training text.")
        return
    cands = scores(follows, prompt)
    if not cands:
        print("  No known continuation for that text.")
        return
    print("  Candidates for the next token:")
    for tok, p in cands:
        print(f"    {tok:<10} {p:5.0%}")
    print("  Most likely path:", generate(follows, prompt, greedy=True))
    print("  Sampled (seed 1):", generate(follows, prompt, seed=1))
    print("  Sampled (seed 2):", generate(follows, prompt, seed=2))


def main():
    ap = argparse.ArgumentParser(description="Tiny next-token predictor")
    ap.add_argument("--prompt", help="run one prompt and exit")
    ap.add_argument("--text", help="path to a text file to learn from")
    args = ap.parse_args()

    if args.text:
        with open(args.text, encoding="utf-8") as f:
            text = f.read()
    else:
        text = DEFAULT_TEXT
    tokens = tokenize(text)
    follows = train(tokens)
    vocab = set(tokens)

    if args.prompt:
        show(follows, vocab, args.prompt)
        return

    if not args.text:
        print("Demo: 'the capital of france is'")
        show(follows, vocab, "the capital of france is")
        print(
            "\nIt picks what is likely in its text, not what is true. "
            "Change the text and the 'facts' change.\n"
        )

    print("Type your own prompt (empty line to quit). Try: the capital of italy is")
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        if not line.strip():
            break
        show(follows, vocab, line)


if __name__ == "__main__":
    main()
