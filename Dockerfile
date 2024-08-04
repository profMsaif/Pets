# using python3.10 image
FROM python:3.13.0rc1-slim

# System deps:
RUN pip install poetry

# set env
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
#ENV PATH="/scripts:/py/bin:$PATH"
ENV PATH="/$VIRTUAL_ENV/bin:$PATH"

WORKDIR /www
EXPOSE 8000
COPY poetry.lock /www/poetry.lock
COPY pyproject.toml /www/pyproject.toml
RUN poetry install --no-root --no-dev

# Project initialization:
COPY . /www/
RUN poetry install --no-dev


CMD ["run.sh"]

