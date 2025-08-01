### 🔄 Project Awareness & Context
- **If starting a new complex task**, read `docs/VISION.md` and `docs/ARCHITECTURE.md` to understand the project's goals.
- **If unsure about current priorities**, check `docs/PLANIFICATION.md`.
- **If looking for examples**, check the `/examples` directory for relevant implementations.
- **Use consistent naming conventions, file structure, and architecture patterns** as described in `docs/ARCHITECTURE.md` and `docs/MCP-DESIGN.md`.
- **Use the virtual environment** whenever executing Python commands, including for unit tests.

### 🧱 Code Structure & Modularity
- **Never create a file longer than 500 lines of code.** If a file approaches this limit, refactor by splitting it into modules or helper files.
- **Organize code into clearly separated MCP servers**, grouped by feature or responsibility.
- **Use clear, consistent imports** (prefer relative imports within packages).
- **Use python_dotenv and load_env()** for environment variables.

### 🧪 Testing & Reliability
- **Always create Pytest unit tests for new features** (functions, classes, routes, etc).
- **After updating any logic**, check whether existing unit tests need to be updated. If so, do it.
- **Tests should live in a `/tests` folder** mirroring the main app structure.

### ✅ Task Completion
- **Ask me to confirm** before marking tasks as completed in `docs/PLANIFICATION.md`.
- **Show me the specific line** you plan to modify before making changes.

### 📎 Style & Conventions
- **Use Python** as the primary language.
- **Follow PEP8**, use type hints, and format with `black`.
- **Use `pydantic` for data validation**.
- Use `FastAPI` for APIs and `SQLAlchemy` or `SQLModel` for ORM if applicable.
- Write **docstrings for every function** using the Google style.

### 📚 Documentation & Explainability
- **Update `README.md`** when new features are added, dependencies change, or setup steps are modified.
- **Comment non-obvious code** and ensure everything is understandable to a mid-level developer.
- When writing complex logic, **add an inline `# Reason:` comment** explaining the why, not just the what.

### 🧠 AI Behavior Rules
- **Never assume missing context. Ask questions if uncertain.**
- **Never hallucinate libraries or functions** – only use known, verified Python packages.
- **Always confirm file paths and module names** exist before referencing them in code or tests.
- **Never delete or overwrite existing code** unless explicitly instructed to or if part of a task from `docs/PLANIFICATION.md`.
- **Ask me which files to examine** rather than reading everything automatically.
- **Only read documentation files when specifically relevant** to the current task.
