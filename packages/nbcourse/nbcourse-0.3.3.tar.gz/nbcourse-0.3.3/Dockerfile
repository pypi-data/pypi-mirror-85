FROM boileaum/jupyter

# From Jupyter Project <jupyter@googlegroups.com>

LABEL maintainer="Matthieu Boileau <matthieu.boileau@math.unistra.fr>"

COPY pyproject.toml .
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="$HOME/.poetry/bin:$PATH"
RUN poetry install