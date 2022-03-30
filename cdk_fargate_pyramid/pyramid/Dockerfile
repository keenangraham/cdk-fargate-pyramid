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

ENV GH_BRANCH=cdk-fargate

ENV GH_USER=IGVF-DACC

ENV GH_REPO=igvfd

ADD https://api.github.com/repos/$GH_USER/$GH_REPO/git/refs/heads/$GH_BRANCH gh_version.json

RUN git clone -b $GH_BRANCH https://github.com/$GH_USER/$GH_REPO.git

WORKDIR /app/igvfd

RUN git rev-parse HEAD > branch_sha.txt

RUN pip install -e .

EXPOSE 80

COPY run.sh ./

RUN chmod +x run.sh

COPY bootstrap.sh ./

RUN chmod +x bootstrap.sh

CMD ["./run.sh"]