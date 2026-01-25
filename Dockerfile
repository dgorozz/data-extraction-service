FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_NO_DEV=1

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN pip install uv --no-cache-dir
RUN uv pip install --system -r pyproject.toml

COPY src/ src/
COPY system-prompt.md /app

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]