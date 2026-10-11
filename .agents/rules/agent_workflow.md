# Agent Workflow & Documentation Rules

These rules govern agent behavior, file creation, documentation upkeep, and git hygiene for this project and across future tasks.

## 1. Documentation & Rationale Upkeep (`AGENTS.md`)
- **Always maintain `AGENTS.md`**: For every task and prompt, update `AGENTS.md` with:
  - The purpose and rationale of every file created.
  - The motivation and technical reasons whenever code is modified from one approach to another.
  - Current architectural state, tool registry, and execution logs.
- Never make arbitrary or unexplained changes; always document the *why*.

## 2. Individual Atomic Commits
- Commit every modified or newly created file individually with clear, conventional commit messages (`feat(...)`, `fix(...)`, `docs(...)`, `refactor(...)`, `chore(...)`).
- Do not batch unrelated files into single monolithic commits.

## 3. GitHub Repository Visibility & Presentation
- Ensure the repository title, description, and topic tags clearly convey the application's true purpose (e.g., "Autonomous Agentic AI Chatbot & Incident Management Platform") so hiring managers, recruiters, and collaborators immediately understand its architectural depth.

## 4. Milestone Completion & Visual Assets
- When a milestone or project build completes:
  1. Provide the exact executable run command for the user (e.g. `python main.py`).
  2. Prompt the user to test the running application, take screenshots, and save them in the `assets/` folder.
  3. Update `README.md` with the latest screenshots, architecture diagrams, and comprehensive feature breakdowns.

## 5. Synchronization
- Keep `README.md`, `IMPLEMENTATION_GUIDE.md`, and `AGENTS.md` synchronized after every feature rollout.
