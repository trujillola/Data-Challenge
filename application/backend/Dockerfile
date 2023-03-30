FROM python:3.10

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ADD app app
VOLUME /app
WORKDIR /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["python", "/app/main.py"]