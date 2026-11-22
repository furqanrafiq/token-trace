# Token Trace

Plain, practical explainers and working code for developers who want to build with LLMs.

Short videos: @tokentraceai on Instagram, TikTok and YouTube, and on LinkedIn.

Each video has its own folder with the script and a small runnable example.

## Videos

| # | Topic | Status |
|---|-------|--------|
| 01 | [How LLMs work (next token prediction)](01-how-llms-work) | Published |
| 02 | Tokens and context windows | Planned |
| 03 | Prompts that survive production | Planned |
| 04 | Tool calling | Planned |
| 05 | Agents and why they fail | Planned |
| 06 | RAG: chunking, embeddings, retrieval vs generation bugs | Planned |
| 07 | Evals, cost, latency and safety | Planned |

Folders for planned videos are added when their work starts.

## How this repo is organized

- `main` is the stable branch. It only contains finished, tested videos.
- Each video is built on its own branch, named `video-NN-topic`, for example `video-01-how-llms-work`.
- A video branch is merged into `main` through a pull request once the example has been run and checked.

## How the examples work

- Every example is run before it is published.
- Examples that need an LLM use the Anthropic API with your own key, read from the `ANTHROPIC_API_KEY` environment variable. Keys are never committed.
- Each folder has its own README with setup steps and expected output.

## Credits

The topic order follows the [Forward Deployed Engineer roadmap](https://github.com/amitshekhariitbhu/forward-deployed-engineer-roadmap) by Amit Shekhar (Apache 2.0). All scripts, text and code here are written independently.

## License

MIT, see LICENSE.
