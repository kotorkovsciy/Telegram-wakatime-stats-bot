FROM python:3.10.1

RUN mkdir -p /usr/src/bot/

WORKDIR /usr/src/bot/

COPY . /usr/src/bot/

RUN pip install -r requirements.txt

CMD ["python", "bot.py"]
