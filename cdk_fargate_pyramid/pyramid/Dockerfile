FROM python:3.9.9-buster

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV=/opt/venv

RUN apt-get update

RUN apt-get install -y make git curl graphviz

RUN python -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python -m pip install --upgrade pip

WORKDIR /app

RUN git clone https://github.com/IGVF-DACC/igvfd.git --branch dev

WORKDIR /app/igvfd

RUN pip install -e .

EXPOSE 6543

CMD ["pserve", "./config/pyramid/ini/local.ini"]