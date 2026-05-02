FROM python:3.11-slim

# Variables de entorno para Python y Poetry
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Añadimos el binario de poetry al PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Instalar dependencias del sistema mínimas
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry usando el script oficial
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

# Copiar archivos de configuración
COPY pyproject.toml README.md ./

# Instalar dependencias
RUN poetry install --no-root

# Copiar el resto del código
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
