## Coding Agent CLI
A command-line coding agent that accepts a coding task and uses a set of predefined functions to inspect and modify a codebase.

## What It Can Do
The agent can choose from the following functions to work on a coding task:
- Scan files — List the files in a directory
- Read files — Read the contents of a file
- Overwrite files — Modify a file by replacing its contents
- Execute Python — Run the Python interpreter on a file
Given a coding task, the agent determines which functions it needs to use to inspect the codebase and make the requested changes.

## Learning Reference 
This project was built as part of the Boot.dev course material and was inspired by the concepts covered there.

## Security Considerations
This project gives an AI agent the ability to read files, modify files, and execute Python code. Depending on the directory you run it against, the agent could potentially access sensitive information or make unintended changes to your system.
- Only run the agent against directories you are comfortable giving it access to.
- Avoid running it in directories containing secrets, credentials, API keys, or other sensitive information.

This project is intended for learning purposes and should not be treated as a secure or sandboxed coding agent.