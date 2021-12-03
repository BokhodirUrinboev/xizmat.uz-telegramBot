FROM python:3.7
RUN mkdir /src
WORKDIR ./src
COPY . .
RUN pip install -r requirements.txt
RUN #pybabel compile -d locales -D testbot