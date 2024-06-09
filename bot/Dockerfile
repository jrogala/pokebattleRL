FROM python:latest

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY . /app

WORKDIR /app

# Presuming there is a `my_app` command provided by the project
CMD ["uv", "run", "src/main.py"]
