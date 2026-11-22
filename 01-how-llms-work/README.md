# 01 How LLMs work

An LLM does not look up answers. It predicts the next token, appends it, and repeats.

Files:
- `video.mp4`: the 30 second explainer
- `script.md`: the voiceover script
- `next_token.py`: a tiny next-token predictor you can run

## Run the example

Needs Python 3, no packages and no API key.

    python next_token.py

It learns from a few lines of text which token tends to follow which, then generates by scoring candidates, picking one, appending it and repeating. Sample output:

    Candidates for the next token:
      paris      80%
      lyon       20%

Run it with different seeds and it sometimes picks "lyon". It picks what is likely in its text, not what is true. Edit `TEXT` and the "facts" change. A real LLM runs the same loop, with a neural network in place of the count table.

## Takeaway

Give the model the real documents it needs, and check its answers.
