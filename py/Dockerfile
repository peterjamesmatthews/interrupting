FROM python:3.12.2-alpine

STOPSIGNAL SIGKILL

EXPOSE 5000

WORKDIR /interrupting/py

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install 

COPY . .

CMD pipenv run flask --app main.py run
