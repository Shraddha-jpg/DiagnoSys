<h1 align="center">Problem Spaces </h1>

This directory contains all problem space definitions, prompts, and tools for the LLM-powered analysis including support for various storage system architectures.

## What is a Problem Space?

A problem space defines a domain (e.g., storage systems) for which the agent can perform root cause analysis, generate reports, and suggest remediations.

## Structure

- Each subfolder (e.g., `storage_system/`) contains:
  - Prompts (`analyze_prompt.txt`, `format_prompt.txt`)
  - Data models (`data_model.json`)
  - Tools (`tools/` with Python scripts)
  - Configuration (`tools.json`)

## Adding a New Problem Space

1. Create a new subfolder under `problem_spaces/`.
2. Add required prompt and config files.
3. Implement any custom tools in a `tools/` subfolder.
4. Update `config.json` to point to the new problem space if needed.

## Example

```
problem_spaces/
  storage_system/
    analyze_prompt.txt
    data_model.json
    format_prompt.txt
    rag.txt
    tools.json
    tools/
      calculate_contribution.py
      volume_contribution_calculator.py
``` 