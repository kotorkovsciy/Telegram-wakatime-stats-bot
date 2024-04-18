FROM python:3.10.1

ENV TZ=Europe/Moscow

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd -ms /bin/bash noroot

RUN mkdir -p /usr/src/bot/

WORKDIR /usr/src/bot/

COPY . /usr/src/bot/

RUN chown -R celery:celery /usr/src/bot/

USER noroot

RUN pip install -r requirements.txt

CMD ["python", "bot.py"]
