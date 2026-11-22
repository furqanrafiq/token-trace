# 01 How LLMs work

An LLM does not look up answers. It predicts the next token, appends it, and repeats.

Files:
- `script.md`: the voiceover script
- `next_token.py`: a tiny next-token predictor you can run

## Run the example

Needs Python 3, no packages and no API key.

    python next_token.py

It first runs a demo, then lets you type your own prompts. Sample output:

    Candidates for the next token:
      paris      80%
      lyon       20%

Try your own:

    python next_token.py --prompt "the capital of italy is"
    python next_token.py --text mytext.txt

The toy model only knows the lines of text it learned from, so use words that appear in them (countries and capitals work). Run it with different seeds and it sometimes picks "lyon". It picks what is likely in its text, not what is true.

## Teach it your own facts

Put a few sentences in a text file, one fact repeated a few times, and run with `--text`. The model repeats whatever your text says, true or not. That is the same weakness a real LLM has, with a neural network in place of the count table.

## Takeaway

Give the model the real documents it needs, and check its answers.
