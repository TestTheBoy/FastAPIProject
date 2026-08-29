# FastAPIProject Agent Guide

## Project map

- `main.py` is the FastAPI application entry point. It wires routers, middleware, startup initialization, static files, and Swagger.
- `App_Demo/` contains shared framework behavior: response models, request/user context, middleware, authentication, exceptions, IOC, and utilities.
- `modules/` contains business modules. Keep the existing split between `controllers/`, `services/`, `models/`, `params/`, `vos/`, and `enums/`.
- `generator/` contains Jinja templates and database-driven code generation. Generated output is controlled by `generator/config.json`.
- `project_pytest/` is the project test area; add focused tests there or beside the behavior being changed when the existing layout requires it.

Read the project overview and dependency assumptions in [README.md](README.md) before changing startup, database, or generator behavior.

## Local workflow

Run commands from the `FastAPIProject` root. Prefer the existing Python 3.11 virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload
pytest
ruff check .
mypy .
```

Use a focused pytest path or a focused `ruff` target first when iterating. The application startup requires a reachable MySQL database configured by `database.py` and a reachable Redis instance; do not treat a startup failure caused by missing services as an application code failure without checking those prerequisites.

The CLI exposes database-backed generation and inspection:

```powershell
python cli.py show --tablename <table>
python cli.py gen --tablename <table>
```

Never run code generation against a real schema as a validation shortcut. Review generated diffs, and remember that configured templates may overwrite existing model and parameter files while other generated files are configured not to overwrite.

## Implementation conventions

- Preserve the controller -> service -> ORM model / parameter / VO layering. Put business rules in services, request and response shapes in Pydantic models, and route wiring in controllers.
- Reuse `CommonResult`/`R`, shared exception enums, `transactional_session`, `UserContext`, and the IOC container instead of introducing parallel mechanisms.
- Match the existing public field naming convention: Python model attributes and API payloads commonly use camelCase while database column names use snake_case.
- Protect authentication and permission behavior. `SaIgnore` and `SaCheckPermission` are part of the route contract, and middleware ordering in `main.py` affects requests.
- Do not commit credentials, tokens, or local database changes. Treat the connection values in `database.py` as development-only and avoid expanding their exposure.
- Keep edits focused and preserve generated/template consistency. If a generated shape changes, update the relevant template and inspect representative generated output.

## Validation expectations

For API changes, run the narrowest relevant pytest tests, then `ruff check` on changed Python files and `mypy` when types or public signatures changed. For middleware, authentication, database, or startup changes, explicitly state whether MySQL and Redis were available during validation. Do not fix unrelated pre-existing diagnostics.
