FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python -m venv /venv

RUN /venv/bin/pip install --upgrade pip wheel setuptools &&\
    /venv/bin/pip install -r requirements.txt

COPY . .

CMD [ "/venv/bin/python", "main.py" ]