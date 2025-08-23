# Base image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim


WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_TOOL_BIN_DIR=/usr/local/bin


RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --locked --no-install-project --no-dev

COPY . /app


RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev


ENV PATH="/app/.venv/bin:$PATH"




ENTRYPOINT []
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
