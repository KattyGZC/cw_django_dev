FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3.8 python3.8-venv python3-pip

WORKDIR /cw_django_dev
COPY . /cw_django_dev

RUN python3.8 -m pip install -r requirements.txt

RUN python3.8 -m venv .pyenv && \
    echo "source .pyenv/bin/activate" >> ~/.bashrc

EXPOSE 8030

CMD ["/cw_django_dev/.pyenv/bin/python", "manage.py", "runserver", "0.0.0.0:8030"]
