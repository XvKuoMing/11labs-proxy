FROM python:3.12-slim-bookworm
# using uv to install dependencies
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app
RUN uv sync --locked

# Default command
CMD ["uv", "run", "main.py"] 