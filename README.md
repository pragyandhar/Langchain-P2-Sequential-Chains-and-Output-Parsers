# Langchain P2: Sequential Chains and Output Parsers

This project demonstrates how to build a multi-step LangChain pipeline that:

1. Generates a structured blog outline using a Pydantic schema.
2. Reshapes that structured output.
3. Produces a final introductory paragraph from the outline.

It focuses on three core concepts:

- Sequential chains with `Runnable` composition.
- Structured output parsing with `PydanticOutputParser`.
- Data enrichment with `RunnablePassthrough.assign(...)`.

## Output

### Project Output Video
https://github.com/user-attachments/assets/3b67c802-b8c3-4518-933f-cfcd2004f4bd

### Project Output Screenshot
[output](assets/output.png)

## Project Structure

```text
.
├── chains.py   # Builds the step-by-step LangChain pipeline
├── main.py     # CLI entry point that runs outline-only and full pipeline
├── prompt.py   # Prompt templates for outline generation and intro expansion
├── schema.py   # Pydantic schema used for structured outline output
└── README.md
```

## How It Works

### 1) Outline Generation (Structured)

In `chains.py`, the pipeline creates an LLM and parser:

- `ChatOpenAI` for generation.
- `PydanticOutputParser(BlogOutline)` for strict JSON-to-schema parsing.

Then it injects parser format instructions into the prompt input using `RunnablePassthrough.assign(...)`, so the model is guided to return output that matches `BlogOutline`.

### 2) Reshaping Intermediate Data

After the outline is parsed, a `RunnableLambda` reshapes the data into the exact input shape expected by the second prompt:

- `title`
- `sections` (joined into a comma-separated string)
- `audience`

### 3) Intro Paragraph Expansion

The reshaped data is passed into `expand_prompt`, then into the LLM, and finally parsed as plain text with `StrOutputParser`.

## Inputs and Outputs

### Input (CLI)

When running `main.py`, you are prompted for:

- Topic
- Target audience
- Number of sections

### Output

The script prints:

1. A structured outline (`title`, `intro`, and section list).
2. A generated 3-4 sentence introduction paragraph from the full pipeline.

## Requirements

- Python 3.10+
- OpenAI API key

Python packages used by the project:

- `langchain-core`
- `langchain-openai`
- `pydantic`
- `python-dotenv`

## Setup

1. Create and activate a virtual environment.
2. Install dependencies.
3. Set your API key in an environment file.

Example:

```bash
python -m venv .venv
source .venv/bin/activate
pip install langchain-core langchain-openai pydantic python-dotenv
```

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
```

## Run

```bash
python main.py
```

## Key Learning Points

- `PydanticOutputParser` is useful when you need reliable, schema-shaped model output.
- `RunnablePassthrough.assign` is a clean way to augment chain input with computed keys.
- Chaining small runnables keeps logic explicit and easier to debug.

## Notes

- The current implementation uses `gpt-3.5-turbo` in the full pipeline and `gpt-4o-mini` for the outline preview in `main.py`.
- The `num_sections` input is collected as text from CLI and passed through prompts as-is.
