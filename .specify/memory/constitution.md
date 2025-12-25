<!-- SYNC IMPACT REPORT
Version change: N/A → 1.0.0
Modified principles: N/A (new constitution)
Added sections: All sections (new constitution)
Removed sections: N/A
Templates requiring updates: 
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated  
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ✅ reviewed
- README.md ⚠ pending
Follow-up TODOs: None
-->
# Todo In-Memory Python Console App Constitution

## Core Principles

### I. Spec-Driven Development
All features must be derived from iterative specifications stored in specs_history folder; use Qwen for spec refinement and code generation. Every implementation step must be traceable back to specific requirements in the specification documents.

### II. Clean Code and Readability
Strict PEP 8 compliance, meaningful names, single-responsibility functions, comprehensive docstrings, type hints everywhere. Code must be self-documenting with clear function and variable names that express intent.

### III. Simplicity and Extensibility
Prioritize clear, maintainable code that is easy to extend in future phases; avoid cleverness or over-engineering. Implement the simplest solution that satisfies requirements while maintaining a clean architecture for future enhancements.

### IV. Professional CLI Experience
User-friendly argparse subcommands, graceful error handling, clean tabular output with visual status indicators ([ ] for pending, [x] for completed). The interface must be intuitive and provide clear feedback for all user actions.

### V. Hackathon Excellence
Demo-ready MVP that clearly demonstrates spec-driven process and high-quality implementation. The application must be polished, reliable, and showcase the development methodology used to create it.

### VI. Test-First Approach
All functionality must be validated through comprehensive testing before deployment. Write tests for normal flows and edge cases (empty list, invalid ID, partial updates) to ensure reliability.

## Technology Stack Requirements

- Python version: 3.13+ exclusively
- Project structure: Package-based under /src/todo/ containing models.py (Task dataclass), storage.py (in-memory operations), cli.py (argparse interface), __init__.py, and __main__.py
- Dependencies: Standard library only; zero external packages
- Task model: Use @dataclass with fields: id (int, auto-increment), title (str), description (str), completed (bool, default False), created_at (datetime)
- In-memory storage: List[Task] managed centrally in storage module with pure functions for all operations

## Feature Requirements

- Storage: Strictly in-memory only; no file or database persistence
- Features: Exactly 5 specified features - Add task, View/List tasks, Update task details by ID, Delete task by ID, Mark task as complete/incomplete (toggle status)
- Error handling: Clear, friendly messages (e.g., "Task with ID X not found")
- CLI commands: argparse subcommands - add, list, update, delete, complete; uv run mani.py <subcommand>
- Output formatting: List command must display ID, Status ([ ]/[x]), Title, truncated Description, Created date; show "No tasks added yet." when empty

## Deliverables

- GitHub repository must include constitution file, specs_history folder with all spec versions, /src with clean code, README.md with setup and usage instructions
- All 5 features fully functional and demonstrable via console commands
- Manual validation passes for normal flows and edge cases (empty list, invalid ID, partial updates)
- Specs history clearly shows iterative spec-driven process
- Code is clean, typed, documented, and fully aligned with constitution
- App runs reliably with UV and provides professional, demo-ready experience

## Governance

This constitution governs all development decisions for the Todo In-Memory Python Console App project. All implementation must align with the stated principles. Amendments to this constitution require explicit documentation of changes, approval from the development team, and a migration plan for existing code.

All pull requests and code reviews must verify compliance with these principles. Code complexity must be justified with clear benefits that outweigh the added complexity. Use this constitution as the primary guidance for all development decisions.

**Version**: 1.0.0 | **Ratified**: 2025-06-13 | **Last Amended**: 2025-12-25