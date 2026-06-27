# Contributing to redisbrowse

Thanks for your interest in contributing! This document covers how to report issues, request features, and submit code changes.

---

## Table of Contents

- [Reporting Bugs](#reporting-bugs)
- [Requesting Features](#requesting-features)
- [Development Setup](#development-setup)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Code Style](#code-style)
- [Commit Messages](#commit-messages)

---

## Reporting Bugs

Use the **Bug Report** issue template on GitHub. Please include:

- A clear description of what went wrong
- Steps to reproduce the issue
- Your environment (OS, Python version, `redis-py` and `textual` versions, Redis server version)
- Any error output or tracebacks

The more detail you provide, the faster we can investigate.

## Requesting Features

Use the **Feature Request** issue template on GitHub. Describe the problem you're trying to solve and your proposed solution. If you have a rough idea rather than a fully formed proposal, open the issue anyway — discussion is welcome.

---

## Development Setup

1. **Fork and clone** the repository:
   ```bash
   git clone https://github.com/QueueForge/redisbrowse.git
   cd redisbrowse
   ```

2. **Create a virtual environment** and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install redis textual
   ```

3. **Start a local Redis instance** (Docker is easiest):
   ```bash
   docker run -p 6379:6379 redis:latest
   ```

4. **Run the tool** against your local instance:
   ```bash
   python redisbrowse.py
   ```

---

## Submitting a Pull Request

1. Create a new branch from `main` with a descriptive name:
   ```bash
   git checkout -b fix/stream-display-encoding
   # or
   git checkout -b feat/key-search-filter
   ```

2. Make your changes. Keep commits focused — one logical change per commit.

3. Test your changes manually against a Redis instance with a variety of key types (list, stream, string, set, hash).

4. Push your branch and open a pull request against `main`. In the PR description, explain:
   - **What** changed and **why**
   - Any trade-offs or open questions
   - How to test it

5. A maintainer will review your PR. Please be patient and responsive to feedback.

### What makes a good PR

- Solves one clearly defined problem
- Doesn't introduce unnecessary dependencies
- Keeps the codebase readable — `redisbrowse` is intentionally simple
- Includes a short description in the PR body

---

## Commit Messages

Use the format `action(file/submodule): message`, for example:

```
fix(redisbrowse): handle binary-encoded stream entry IDs
feat(ui): add key search filter to the keys panel
refactor(RedisTUI): split Redis type dispatch into separate methods
docs(CONTRIBUTING): clarify PR review process
chore(deps): pin textual to >= 0.50
```

---

By contributing, you agree that your changes will be licensed under the project's [MIT License](LICENSE).