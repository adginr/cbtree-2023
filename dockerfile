FROM python:3.11-bullseye

ENV POETRY_VERSION=1.4.2\
  PIP_DISABLE_PIP_VERSION_CHECK=1

# Create working dir
WORKDIR /code

# Copy the project's pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

RUN pip install "poetry==${POETRY_VERSION}" &&\
  poetry export -f requirements.txt -o requirements.txt &&\ 
  pip install -r requirements.txtkz

COPY . .


EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
